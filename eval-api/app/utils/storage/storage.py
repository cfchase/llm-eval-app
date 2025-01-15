from abc import ABC, abstractmethod
from PIL import Image


class Storage(ABC):
    @abstractmethod
    def make_dirs(self, dir_path: str):
        pass

    @abstractmethod
    def list_files(self, dir_path, pattern: str, recursive: bool = False):
        pass

    @abstractmethod
    def write_json(self, data, file_path: str):
        pass

    @abstractmethod
    def read_json(self, file_path: str) -> dict:
        pass

    @abstractmethod
    def write_file(self, data: bytes, file_path: str):
        pass

    @abstractmethod
    def read_file(self, file_path: str) -> bytes:
        pass

