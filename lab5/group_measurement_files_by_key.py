from pathlib import Path
import re

_re_expression = re.compile(r"^(?P<year>\d{4})_(?P<type>.+)_(?P<frequency>\w+)\.csv$")


def group_measurement_files_by_key(dir_: Path):
    result = {}
    try:
        files = [file for file in dir_.iterdir() if file.is_file()]
    except (FileNotFoundError, NotADirectoryError, PermissionError):
        return result
    for file in files:
        found = re.match(_re_expression, file.name)
        if found:
            result[
                (found.group("year"), found.group("type"), found.group("frequency"))
            ] = file
    return result
