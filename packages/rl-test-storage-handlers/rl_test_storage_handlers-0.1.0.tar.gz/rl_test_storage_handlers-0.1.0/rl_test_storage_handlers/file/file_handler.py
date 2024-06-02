from abc import abstractmethod

from rl_test_common import Common

from ..params.storage_data import StorageData
from ..params.storage_destination import StorageDestination
from ..storage_handler import StorageHandler
from .params.file_data import FileData
from .params.file_destination import FileDestination


class FileHandler(StorageHandler):
    __common: Common = Common()

    @abstractmethod
    def write(self, destination: StorageDestination, data: StorageData) -> None:
        pass

    @abstractmethod
    def read(self, destination: StorageDestination) -> StorageData:
        pass

    def _write(self, destination: FileDestination, mode: str, data: FileData) -> None:
        file_path: str = self.__get_file_path(destination.get())

        with open(file_path, mode) as file:
            file.write(data.get())

    def _read(self, destination: FileDestination, mode: str) -> FileData:
        file_path: str = self.__get_file_path(destination.get())
        data: FileData | None = None

        with open(file_path, mode) as file:
            data = FileData(file.read())

        return data

    def __get_file_path(self, file_name: str) -> str:
        return f'{self.__common.user_files_root}/{file_name}'
