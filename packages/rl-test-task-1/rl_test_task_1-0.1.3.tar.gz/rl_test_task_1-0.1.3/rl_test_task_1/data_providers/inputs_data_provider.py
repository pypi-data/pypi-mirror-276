from typing import Sequence

from rl_test_storage_handlers.params.storage_data import StorageData
from rl_test_storage_handlers.params.storage_destination import \
    StorageDestination
from rl_test_storage_handlers.storage_handler import StorageHandler

from .data_provider import DataProvider
from .models.input import Input


class InputsDataProvider(DataProvider):
    __inputs: list[Input] = []

    def __init__(self, storage_handler: StorageHandler,
                 destinations: Sequence[StorageDestination]) -> None:
        for destination in destinations:
            data: StorageData = storage_handler.read(destination)
            self.__inputs.append(Input(data.get()))

    def get(self) -> list[Input]:
        return self.__inputs
