import glob
import io
import os
import json
from .storage import Storage
from PIL import Image


class FileStorage(Storage):
    def __init__ (self, base_storage_path):
        self.base_storage_path = base_storage_path

    def make_dirs(self, dir_path):
        os.makedirs(os.path.join(self.base_storage_path, dir_path), exist_ok=True)

    def list_files(self, dir_path, pattern, recursive=False):
        path = os.path.join(self.base_storage_path, dir_path, pattern)
        files = glob.glob(path, recursive=recursive)
        return [f.replace(f"{self.base_storage_path}/", "", 1) for f in files]

    def write_json(self, data, file_path):
        with open(os.path.join(self.base_storage_path, file_path), "w") as f:
            json.dump(data, f, indent=2)

    def read_json(self, file_path):
        with open(os.path.join(self.base_storage_path, file_path), "r") as f:
            return json.load(f)

    def write_file(self, data: bytes, file_path: str):
        with open(os.path.join(self.base_storage_path, file_path), 'wb') as f:
            f.write(data)

    def read_file(self, file_path: str):
        with open(os.path.join(self.base_storage_path, file_path), 'rb') as f:
            file_data = f.read()
            return file_data



