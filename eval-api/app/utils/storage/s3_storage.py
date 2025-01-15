import fnmatch
import os
import io
import re
import json
import boto3
import botocore
from .storage import Storage
from PIL import Image


class S3Storage(Storage):
    def __init__ (self, aws_access_key_id, aws_secret_access_key, endpoint_url, region_name, bucket_name, s3_prefix):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.region_name = region_name
        self.bucket_name = bucket_name

        self.session = boto3.session.Session(aws_access_key_id=aws_access_key_id,
                                        aws_secret_access_key=aws_secret_access_key)
        self.s3_resource = self.session.resource(
            's3',
            config=botocore.client.Config(signature_version='s3v4'),
            endpoint_url=endpoint_url,
            region_name=region_name)

        self.bucket = self.s3_resource.Bucket(bucket_name)
        self.s3_prefix = s3_prefix

    def make_dirs(self, dir_path: str):
        pass

    def list_files(self, dir_path: str, pattern: str, recursive=False):
        filter = self.bucket.objects.filter(Prefix=os.path.join(self.s3_prefix, dir_path))
        filenames = [f.key for f in filter.all()]
        if self.s3_prefix:
            filenames = [fn.replace(f"{self.s3_prefix}/", "", 1) for fn in filenames]
        regex = fnmatch.translate(pattern)
        reobj = re.compile(regex)
        filtered_files = [f for f in filenames if reobj.match(f)]
        return filtered_files

    def write_json(self, data: dict, file_path: str):
        key = os.path.join(self.s3_prefix, file_path)
        body = bytes(json.dumps(data, indent=2).encode('UTF-8'))
        self.bucket.put_object(Key=key, Body=body)

    def read_json(self, file_path) -> dict:
        key = os.path.join(self.s3_prefix, file_path)
        file_content = self.bucket.Object(key).get()['Body'].read().decode('utf-8')
        return json.loads(file_content)

    def write_file(self, bytes_data: bytes, file_path):
        key = os.path.join(self.s3_prefix, file_path)
        self.bucket.put_object(Key=key, Body=bytes_data)

    def read_file(self, file_path: str) -> bytes:
        key = os.path.join(self.s3_prefix, file_path)
        return self.bucket.Object(key).get()['Body']


