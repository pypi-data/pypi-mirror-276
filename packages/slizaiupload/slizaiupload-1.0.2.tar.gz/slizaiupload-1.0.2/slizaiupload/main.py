import aiohttp
import asyncio
import os
import aiofiles
import logging
from tenacity import retry, stop_after_attempt, wait_fixed
import argparse
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logging.basicConfig(filename='upload_errors.log', level=logging.ERROR, 
                    format='%(asctime)s:%(levelname)s:%(message)s')
logging.basicConfig(filename='upload_debug.log', level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

TOKEN = ""
NUMBER_THREAD = 20
RETRY_DELAY_SECONDS = 300

class UploadErrorException(Exception):
    def __init__(self, file_path, key, message=None):
        self.file_path = file_path
        self.key = key
        self.message = message or f"Failed to upload {file_path}"
        super().__init__(self.message)

# Retry configuration
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), retry_error_callback=lambda retry_state: retry_state.outcome.result())
async def retry_request(request_coro):
    return await request_coro

def getToken():
    if os.getenv('TOKEN') is not None:
        token = os.getenv('TOKEN')
    else:
        token = TOKEN
    return f"Bearer {token}"

async def create_object(session, api_url, version, size_bytes, key):
    url = f"{api_url}/api/v{version}/SLizAI/CreateObject"
    data = {
        "sizeBytes": size_bytes,
        "key": key
    }
    headers = {
        "Authorization": f"{getToken()}"
    }
    async with session.post(url, json=data, headers=headers) as response:
        response.raise_for_status()
        return await response.json()

async def create_part(session, api_url, version, signature, part_number, upload_id):
    url = f"{api_url}/api/v{version}/SLizAI/CreatePart"
    data = {
        "signature": signature,
        "partNumber": part_number,
        "uploadId": upload_id
    }
    headers = {
        "Authorization": f"{getToken()}"
    }
    async with session.post(url, json=data, headers=headers) as response:
        response.raise_for_status()
        return await response.json()

async def complete_part(session, api_url, version, signature, part_etags, upload_id):
    url = f"{api_url}/api/v{version}/SLizAI/CompletePart"
    data = {
        "signature": signature,
        "partEtags": part_etags,
        "uploadId": upload_id
    }
    headers = {
        "Authorization": f"{getToken()}"
    }
    async with session.post(url, json=data, headers=headers) as response:
        response.raise_for_status()
        print(f"complete_part OK")
        return await response.json()

async def upload_part(session, presigned_url, part_data):
    async with session.put(presigned_url, data=part_data) as response:
        response.raise_for_status()
        print(f"upload_part OK {presigned_url}")
        return response.headers['ETag']
    
async def upload_whole_file(session, presigned_url, file_path):
    async with aiofiles.open(file_path, 'rb') as file:
        file_data = await file.read()
        async with session.put(presigned_url, data=file_data) as response:
            print(f"upload_whole_file OK {presigned_url}")
            response.raise_for_status()
            return True

async def upload_file_multipart(session, api_url, version, file_path, key, semaphore):
    async with semaphore:
        print(f"Start upload {key}")
        size_bytes = os.path.getsize(file_path)
        try:
            # Step 1: Create Object
            create_object_response = await retry_request(create_object(session, api_url, version, size_bytes, key))
            signature = create_object_response['data']['signature']
            upload_id = create_object_response['data']['uploadPartId']
            presigned_url = create_object_response['data']['presignedURL']

            if upload_id:
                # Step 2: Upload Parts
                part_etags = []
                part_number = 1
                chunk_size = 5 * 1024 * 1024  # 5MB

                async with aiofiles.open(file_path, 'rb') as file:
                    while True:
                        part_data = await file.read(chunk_size)
                        if not part_data:
                            break
                        
                        create_part_response = await retry_request(create_part(session, api_url, version, signature, part_number, upload_id))
                        presigned_url = create_part_response['data']['presignedURL']
                        e_tag = await retry_request(upload_part(session, presigned_url, part_data))
                        
                        part_etags.append({
                            "partNumber": part_number,
                            "eTag": e_tag
                        })
                        part_number += 1

                # Step 3: Complete Parts
                complete_part_response = await retry_request(complete_part(session, api_url, version, signature, part_etags, upload_id))
                return complete_part_response
            else:
                upload_full_file_response = await retry_request(upload_whole_file(session, presigned_url, file_path))
                return upload_full_file_response
        except Exception as e:
            logging.error(f"Failed to upload {file_path}: {str(e)}")
            custom_exception = UploadErrorException(file_path, key, str(e))
            custom_exception.key = key
            raise custom_exception

async def retry_failed_uploads(api_url, version, failed_files):
    if not failed_files:
        return

    print(f"Retry upload")
    await asyncio.sleep(RETRY_DELAY_SECONDS)  # Wait for 5 minutes
    semaphore = asyncio.Semaphore(NUMBER_THREAD)
    async with aiohttp.ClientSession() as session:
        tasks = [upload_file_multipart(session, api_url, version, file_path, key, semaphore) 
                 for file_path, key in failed_files]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        new_failed_files = []
        for result in results:
            if isinstance(result, Exception):
                new_failed_files.append((result.file_path, result.key))
        
        if new_failed_files:
            await retry_failed_uploads(api_url, version, new_failed_files)

async def upload_folder(api_url, version, folder_path, include_folder, parent_folder_name):
    semaphore = asyncio.Semaphore(NUMBER_THREAD)
    async with aiohttp.ClientSession() as session:
        tasks = []
        failed_files = []
        for root, dirs, files in os.walk(folder_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
            for file in files:
                file_path = os.path.join(root, file)
                if parent_folder_name:
                    key = f"{parent_folder_name}/{os.path.relpath(file_path, os.path.dirname(folder_path)).replace(os.sep, '/')}"
                elif include_folder:
                    key = os.path.relpath(file_path, os.path.dirname(folder_path)).replace(os.sep, '/')
                else:
                    key = os.path.relpath(file_path, folder_path).replace(os.sep, '/')
                tasks.append(upload_file_multipart(session, api_url, version, file_path, key, semaphore))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                print(f"An error occurred: {(result.file_path, result.key)}")
                failed_files.append((result.file_path, result.key))
            #else:
            #    print(f"Multipart upload completed successfully")
        
        if failed_files:
            await retry_failed_uploads(api_url, version, failed_files)

def main():
    current_dir = Path(os.getcwd())
    parser = argparse.ArgumentParser(description="Upload folder to API with multipart upload.")
    parser.add_argument('folder_path', type=str, help='Path to the folder to upload')
    parser.add_argument('--include-folder', action='store_true', help='Include folder path in key')
    parser.add_argument('--parent-folder-name', type=str, help='Parent folder name to include in key')
    parser.add_argument('--thread', type=int, help='Number of threads upload')
    parser.add_argument('--retry-delay', type=int, help='time delay (in seconds) before retrying')
    parser.add_argument('--env', type=str, help='path file ENV')
    args = parser.parse_args()
    if args.env:
        dotenv_path = os.path.join(args.env, '.env')
    else:
        dotenv_path = current_dir / '.env'
    load_dotenv(dotenv_path)
    api_url = os.getenv('API_URL')
    version = os.getenv('VERSION') or 1
    global TOKEN
    TOKEN = os.getenv('TOKEN')

    if not api_url or not version:
        raise ValueError("API_URL and TOKEN environment variables must be set")
    
    folder_path = args.folder_path
    include_folder = args.include_folder
    parent_folder_name = args.parent_folder_name
    global NUMBER_THREAD, RETRY_DELAY_SECONDS
    if args.thread:
        NUMBER_THREAD = args.thread
    if args.retry_delay:
        RETRY_DELAY_SECONDS = args.retry_delay
    try:
        asyncio.run(upload_folder(api_url, version, folder_path, include_folder, parent_folder_name))
    except Exception as e:
        print("An error occurred during the upload process:", str(e))

if __name__ == "__main__":
    try:
        main()
        print("Upload Done")
    except Exception as e:
        print("Error occurred:", str(e))
