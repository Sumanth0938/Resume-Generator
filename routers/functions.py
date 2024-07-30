import os
import io
import re
from PIL import Image
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import mimetypes

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'drive_api_service_account_credentials.json'

# Authenticate using service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/drive"]
)

# Build the Drive API client
service = build('drive', 'v3', credentials=credentials)



def upload_to_drive(file_path,  folder_id=None):

        file_metadata = {
            'name': os.path.basename(file_path)
        }
        mime_type, _ = mimetypes.guess_type(file_path)

        if mime_type is None:
            mime_type = 'application/octet-stream'

        if folder_id:
            file_metadata['parents'] = [folder_id]

        media = MediaFileUpload(file_path, mimetype=mime_type)

        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        return file.get("id")

def download_file(file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    # Create a directory named 'downloads' in the same location where this script exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_folder = os.path.join(script_dir, 'downloads')
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)

    f_name = service.files().get(fileId=file_id, fields='name').execute()

    # Save the file to the 'downloads' folder
    file_path = os.path.join(downloads_folder, f_name.get('name'))

    with open(file_path, 'wb') as f:
        f.write(fh.getvalue())
    return file_path
