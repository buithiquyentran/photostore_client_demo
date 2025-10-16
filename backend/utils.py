from typing import List
import requests
from fastapi import FastAPI, HTTPException, UploadFile, File,Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import hmac, hashlib, time
app = FastAPI()

# Cho phép React call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import uuid
from datetime import datetime
import os

app = FastAPI()

DATA_FILE = "products.json"

API_BASE = "http://localhost:8000"  
API_KEY = "pk_9Z_1XFr9SOoIKGQHzhqzYrSof2w_ij1HzXZE9tbvrQ8"
API_SECRET = "sk_gOO1lx5TFJD9-IPhsukv7KRMGrcMlB1goRg5AObc9y6u3jceewmIQm9oitYhx186"

def get_signature():
    timestamp = int(time.time())
    message = f"{timestamp}:{API_KEY}"
    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return {"signature": signature, "timestamp": timestamp}


def get_image(file_url: str):
    sig = get_signature()
    res = requests.get(
        f"{file_url}", #http://localhost:8000/uploads/5/project1/new-folder/3f51f03e646b46f6b9d499072bb40afe.jpg
       headers = {
        "X-API-Key": API_KEY,
        "X-Signature": sig["signature"],
        "X-Timestamp": str(sig["timestamp"]),
    },
        stream=True
    )

    if res.status_code != 200:
        raise HTTPException(res.status_code, "Cannot fetch private asset")

    return StreamingResponse(res.iter_content(chunk_size=1024),
                             media_type=res.headers.get("content-type"))

def delete_image(path: str):
    sig = get_signature()
    res = requests.delete(
        f"{API_BASE}/api/external/assets?file_url={path}", #http://localhost:8000/uploads/5/project1/home/af90399f0c464783b30b93e46cf19853.jpg
        headers = {
        "X-API-Key": API_KEY,
        "X-Signature": sig["signature"],
        "X-Timestamp": str(sig["timestamp"]),
    },
        stream=True
    )

    if res.status_code != 200:
        raise HTTPException(res.status_code, "Cannot fetch private asset")

    return StreamingResponse(res.iter_content(chunk_size=1024),
                             media_type=res.headers.get("content-type"))


async def upload_files(files: List[UploadFile] = File(...)):
    sig = get_signature()
     # build danh sách files để gửi đi
    files_data = []
    for file in files:
        content = await file.read()
        files_data.append(("files", (file.filename, content, file.content_type)))
    # gọi /upload với file + api_key + signature + timestamp
    upload_res = requests.post( 
        f"{API_BASE}/api/external/assets/upload",
        files=files_data,
        data={"folder_slug": "home1","is_private": "true",}, 
        headers = {
        "X-API-Key": API_KEY,
        "X-Signature": sig["signature"],
        "X-Timestamp": str(sig["timestamp"]),
    },
    )

    return upload_res.json()
