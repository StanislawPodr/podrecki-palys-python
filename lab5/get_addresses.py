from pathlib import Path
import re

from csv_parser import get_station_data

_street_and_number_re = re.compile(
    r"^(?P<street>.*?)(?: (?P<number>\d+[a-zA-Z0-9\-/]*))?$"
)


def get_addresses(path: Path, city: str):
    result = []
    if not path.is_file():
        return result
    with open(path, "r") as file:
        stations_data = get_station_data(file)
        for station in stations_data.values():
            if station["Miejscowość"].lower() == city.lower():
                found = re.match(_street_and_number_re, station["Adres"])
                if found:
                    result.append(
                        (
                            station["Województwo"],
                            city,
                            found.group("street"),
                            found.group("number"),
                        )
                    )
    return result
