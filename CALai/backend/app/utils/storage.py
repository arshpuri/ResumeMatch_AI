"""
S3/MinIO file storage operations.
"""

import io
import uuid
from typing import BinaryIO

import boto3
from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError

from app.config import get_settings

settings = get_settings()


def _get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        config=BotoConfig(signature_version="s3v4"),
        region_name="us-east-1",
    )


def ensure_bucket_exists():
    """Create the resumes bucket if it doesn't exist."""
    client = _get_s3_client()
    try:
        client.head_bucket(Bucket=settings.S3_BUCKET_NAME)
    except ClientError:
        client.create_bucket(Bucket=settings.S3_BUCKET_NAME)


def upload_file(
    file_data: BinaryIO,
    original_filename: str,
    content_type: str = "application/octet-stream",
) -> str:
    """Upload file to S3, returns the object key."""
    client = _get_s3_client()
    ext = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "bin"
    object_key = f"resumes/{uuid.uuid4()}.{ext}"

    client.upload_fileobj(
        file_data,
        settings.S3_BUCKET_NAME,
        object_key,
        ExtraArgs={"ContentType": content_type},
    )
    return object_key


def download_file(object_key: str) -> bytes:
    """Download a file from S3 and return its bytes."""
    client = _get_s3_client()
    buf = io.BytesIO()
    client.download_fileobj(settings.S3_BUCKET_NAME, object_key, buf)
    buf.seek(0)
    return buf.read()


def delete_file(object_key: str):
    """Delete a file from S3."""
    client = _get_s3_client()
    client.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=object_key)


def get_presigned_url(object_key: str, expires_in: int = 3600) -> str:
    """Generate a presigned URL for file download."""
    client = _get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET_NAME, "Key": object_key},
        ExpiresIn=expires_in,
    )
