import os
import re
import shutil
import logging
import json
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from googleapiclient.discovery import build
from google.oauth2 import service_account

from infra.database import SessionLocal
import utilities.logger as Logger
from routers.functions import upload_to_drive, download_file

error_logger = Logger.get_logger("error", logging.ERROR)
info_logger = Logger.get_logger("info", logging.INFO)

from models.resume import Resume

router = APIRouter(prefix="/resume", tags=["resume"])

# Path to your service account key file
SERVICE_ACCOUNT_FILE = r"C:\Users\kalya\OneDrive\Desktop\Resume-Generator\drive_api_service_account_credentials.json"
                        
# Authenticate using service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/drive"]
)

# Build the Drive API client
service = build("drive", "v3", credentials=credentials)

# Google Drive folder ID
FOLDER_ID = "1BzJPVjxVDi3SHxMIEdLqThaVS0S0W8Rn"

# Local directory path
LOCAL_DIRECTORY_PATH = r"C:\Users\kalya\OneDrive\Pictures\resumes"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[SessionLocal, Depends(get_db)]


@router.post("/copy-pdf/")
async def copy_pdf(source_path: str, destination_path: str, db: db_dependency):
    try:
        source_path = source_path.strip('"')
        destination_path = destination_path.strip('"')
        source = Path(source_path)
        destination_dir = Path(destination_path)
        destination = destination_dir / source.name

        if not source.is_file():
            raise HTTPException(status_code=404, detail="Source PDF file not found.")

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(source), str(destination))

        return {
            "message": "PDF file copied successfully.",
            "destination_path": str(destination),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/drive_api/upload_json/")
async def upload_json(data: dict, db: db_dependency):
    try:
        # Get the value of the "name" field from the JSON data
        name = data.get("name")

        max_id = db.query(func.max(Resume.id)).scalar() or 0
        max_id += 1

        # Convert the JSON data to a string
        json_str = str(data)

        # Save the JSON data to a temporary file
        file_path = f"./{str(max_id)}.json"
        with open(file_path, "w") as file:
            file.write(json_str)

        # Save the JSON file to the local directory
        local_file_path = os.path.join(LOCAL_DIRECTORY_PATH, f"{str(max_id)}.json")
        shutil.copy(file_path, local_file_path)

        # Upload JSON file to Google Drive
        file_id = upload_to_drive(file_path, FOLDER_ID)

        if not file_id:
            return JSONResponse(
                {"message": "Upload files to drive failed"}, status_code=500
            )

        # Adding data to the database
        db_resume = Resume(id=max_id, username=name)
        db.add(db_resume)
        db.commit()

        os.remove(file_path)
        return JSONResponse(
            {"message": "File uploaded to drive successfully", "file_id": file_id},
            status_code=200,
        )

    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=500)



@router.get("/drive_api/list_files/")
async def list_files():
    try:
        response = (
            service.files()
            .list(
                q=f"'{FOLDER_ID}' in parents", spaces="drive", fields="files(id, name)"
            )
            .execute()
        )
        files = response.get("files", [])
        return {"files": files}
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=500)


@router.post("/download_images_from_gdrive")
def download_files(drive_link: str):
    try:
        pattern = r"https?://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/([^/]+)/?"
        match = re.match(pattern, drive_link)

        if match:
            file_id = match.group(1)
            filename = match.group(2)
            file_path = download_file(file_id, filename)

            if not file_path:
                return JSONResponse(
                    {"message": "Download files from drive failed"}, status_code=500
                )
            return JSONResponse(
                {"detail": "File downloaded successfully to downloader folder"},
                status_code=200,
            )
        else:
            return JSONResponse(
                {"detail": "Invalid Google Drive link format."}, status_code=403
            )
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=500)
