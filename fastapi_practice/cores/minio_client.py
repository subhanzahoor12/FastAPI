from minio import Minio
from fastapi_practice.cores.config import MINIO_ROOT_USER, MINIO_ROOT_PASSWORD

minio_client = Minio(
    "127.0.0.1:9000",
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=False
)
