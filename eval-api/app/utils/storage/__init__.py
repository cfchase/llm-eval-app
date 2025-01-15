from .storage import Storage
from .s3_storage import S3Storage
from .file_storage import FileStorage
from ..config import logger

import os


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT = os.environ.get("AWS_S3_ENDPOINT")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")
AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET")
AWS_S3_PREFIX = os.environ.get("AWS_S3_PREFIX", "llm-eval/")


BASE_STORAGE_PATH = os.environ.get("BASE_STORAGE_PATH", "/tmp/llm-eval/")

if AWS_ACCESS_KEY_ID:
    logger.info("using S3Storage")
    storage: Storage = S3Storage(AWS_ACCESS_KEY_ID,
                                 AWS_SECRET_ACCESS_KEY,
                                 AWS_S3_ENDPOINT,
                                 AWS_DEFAULT_REGION,
                                 AWS_S3_BUCKET,
                                 AWS_S3_PREFIX)
else:
    logger.info(f"using FileStorage at base: {BASE_STORAGE_PATH}")
    storage: Storage = FileStorage(BASE_STORAGE_PATH)
