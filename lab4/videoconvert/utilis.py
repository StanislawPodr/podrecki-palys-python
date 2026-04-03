from datetime import datetime
from pathlib import Path
from os import environ, path
import argparse

DEFAULT_DIR_NAME = './converted/'


def get_path_to_output(format_: str, input_file: Path) -> Path:
    now = datetime.now()
    date = now.strftime("%Y%m%d")

    # Nazwa pliku wynikowego ma format data-nazwa_pliku_wejsciowego.format
    file_name = f'{date}-{input_file.stem}.{format_}'
    # Ścieżka do rezultatu jest zawarta w zmiennej środowiskowej, albo domyślnie DEFAULT_DIR_NAME
    file_path = Path(environ.get('CONVERTED_DIR', DEFAULT_DIR_NAME))

    return file_path / file_name

def check_input_file(support_decode: set[str]):
    def check_input_file_helper(path_str: str):
        path_ = Path(path_str)
        if not path_.is_file():
            raise argparse.ArgumentTypeError(f"{path_str} is not a file!")
        extension = path_.suffix.removeprefix(".").lower()
        if extension not in support_decode:
            raise argparse.ArgumentTypeError('Input file format not supported')
        return path_
    return check_input_file_helper


def check_output_file(support_encode: set[str]):
    def check_output_file_helper(format_: str):
        if format_ not in support_encode:
            raise argparse.ArgumentTypeError('Output file format not supported')
        return format_
    return check_output_file_helper
