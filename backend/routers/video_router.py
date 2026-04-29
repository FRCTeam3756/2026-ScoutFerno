import os
from base64 import b64encode

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..security.google_auth_guard import require_auth

router = APIRouter(prefix="/videos", tags=["videos"], dependencies=[Depends(require_auth)])

CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_STREAM_TOKEN = os.getenv("CLOUDFLARE_STREAM_TOKEN")


class DirectUploadRequest(BaseModel):
    file_size: int
    file_name: str
    max_duration_seconds: int = 600


def encode_metadata_value(value: str) -> str:
    return b64encode(value.encode("utf-8")).decode("utf-8")


@router.post("/direct-upload")
async def create_direct_upload(payload: DirectUploadRequest):
    if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_STREAM_TOKEN:
        raise HTTPException(status_code=500, detail="Cloudflare env vars are missing")

    upload_metadata = ",".join(
        [
            f"name {encode_metadata_value(payload.file_name)}",
            f"maxDurationSeconds {encode_metadata_value(str(payload.max_duration_seconds))}",
        ]
    )

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT_ID}/stream?direct_user=true"
    )

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_STREAM_TOKEN}",
        "Tus-Resumable": "1.0.0",
        "Upload-Length": str(payload.file_size),
        "Upload-Metadata": upload_metadata,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, headers=headers)

    if response.status_code not in (200, 201):
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Failed to create Cloudflare upload URL",
                "status_code": response.status_code,
                "body": response.text,
            },
        )

    upload_url = response.headers.get("Location")
    if not upload_url:
        raise HTTPException(status_code=500, detail="Cloudflare did not return Location header")

    video_uid = upload_url.rstrip("/").split("/")[-1]

    return {
        "upload_url": upload_url,
        "video_uid": video_uid,
    }
