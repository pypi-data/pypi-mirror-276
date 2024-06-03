from rl_test_storage_handlers.file.params.file_destination import \
    FileDestination
from rl_test_storage_handlers.file.text_file_handler import TextFileHandler

from .data_exporters.persons_data_exporter import PersonsDataExporter
from .data_providers.inputs_data_provider import InputsDataProvider
from .data_providers.persons_data_provider import PersonsDataProvider


class Client:
    def client_code(self) -> None:
        text_file_handler: TextFileHandler = TextFileHandler()
        inputs_data_provider: InputsDataProvider = InputsDataProvider(
            text_file_handler, self.__get_input_file_destinations())
        persons_data_provider: PersonsDataProvider = PersonsDataProvider(
            inputs_data_provider)
        persons_data_exporter: PersonsDataExporter = PersonsDataExporter(
            text_file_handler, persons_data_provider)
        output_file_destination: FileDestination = FileDestination(
            'output.txt')
        persons_data_exporter.export_sorted(output_file_destination)

    def __get_input_file_destinations(self) -> list[FileDestination]:
        file_names: list[str] = ['first_names.txt', 'last_names.txt']

        return [FileDestination(file_name) for file_name in file_names]
