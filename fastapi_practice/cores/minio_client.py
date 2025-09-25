from minio import Minio
from fastapi_practice.cores.config import MINIO_ROOT_USER, MINIO_ROOT_PASSWORD
import os

minio_client = Minio(
    "127.0.0.1:9000",
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=False
)
async def check_minio_bucket(bucket_name: str):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
    return True

async def put_object_in_minio(bucket_name: str, object_name: str, file):
    minio_client.put_object(
        bucket_name,
        object_name,
        file,
        length=-1,
        part_size=10 * 1024 * 1024,
    )
    return True

async def get_object_from_minio(bucket_name: str, object_name: str):
    return minio_client.get_object(bucket_name, object_name)            

async def delete_object_from_minio(bucket_name, object_name):
    return minio_client.remove_object(bucket_name, object_name)

async def update_object_in_minio(path: str, file):
    object_name = os.path.basename(path)
    bucket_name = os.path.basename(os.path.dirname(path))

    await delete_object_from_minio(bucket_name, object_name)
    file_extension = os.path.splitext(file.filename)[1]

    new_object_name = f"image_{os.urandom(8).hex()}{file_extension}"

    await put_object_in_minio(bucket_name, new_object_name, file.file)
    image_path = f"/{bucket_name}/{new_object_name}"
    
    return image_path