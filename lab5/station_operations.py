from itertools import repeat
import re
from typing import Iterable

from csv_parser import get_station_data

_dates_re = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
_with_dash_re = re.compile(r"^[^-]+-[^-]+$")
_polish_diacritics = {
    "ą": "a",
    "ć": "c",
    "ę": "e",
    "ł": "l",
    "ń": "n",
    "ó": "o",
    "ś": "s",
    "ź": "z",
    "ż": "z",
    "Ą": "A",
    "Ć": "C",
    "Ę": "E",
    "Ł": "L",
    "Ń": "N",
    "Ó": "O",
    "Ś": "S",
    "Ź": "Z",
    "Ż": "Z",
}


def _get_dates_from_record(station_data):
    opening_date = station_data.get("Data uruchomienia")
    closing_date = station_data.get("Data zamknięcia")
    open_match = re.match(_dates_re, opening_date) if opening_date else None
    close_match = re.match(_dates_re, closing_date) if closing_date else None
    op_yr = op_mnth = op_d = cl_yr = cl_mnth = cl_d = None
    if open_match:
        op_yr = int(open_match.group("year"))
        op_mnth = int(open_match.group("month"))
        op_d = int(open_match.group("day"))
    if close_match:
        cl_yr = int(close_match.group("year"))
        cl_mnth = int(close_match.group("month"))
        cl_d = int(close_match.group("day"))
    return ((op_yr, op_mnth, op_d), (cl_yr, cl_mnth, cl_d))


def get_dates(csv_data: Iterable):
    stations_data = get_station_data(csv_data)
    result = {}
    for key, vals in stations_data.items():
        result[key] = _get_dates_from_record(vals)
    return result


def _get_geo_coords_from_record(station_data):
    north = station_data.get("WGS84 φ N")
    east = station_data.get("WGS84 λ E")
    try:
        return float(north), float(east)
    except (TypeError, ValueError):
        return None, None


def get_geo_coords(csv_data: Iterable):
    stations_data = get_station_data(csv_data)
    result = {}
    for key, vals in stations_data.items():
        result[key] = _get_geo_coords_from_record(vals)
    return result


def get_with_dashes(csv_data: Iterable):
    stations_data = get_station_data(csv_data)
    result = []
    for key, vals in stations_data.items():
        station_name = vals.get("Nazwa stacji")
        if station_name:
            dash_match = re.match(_with_dash_re, station_name)
            if dash_match:
                result.append(key)
    return result


# Funckcja zmieniająca znaki polskie na ich łacińskie
# Jest lepszy sposób żeby to zrobić na pewno ale raczej nie z regexem
def _remove_diacritics(text):
    result = re.sub(
        "[" + "".join([key for key in _polish_diacritics]) + "]",
        lambda x: _polish_diacritics[x.group()],
        text,
    )
    return result


def _with_spaces_to_snake(text):
    return re.sub(" ", "_", text)


def remove_diacritics_and_spaces_in_station_names(csv_data):
    stations_data = get_station_data(csv_data)
    result = {}
    for key, vals in stations_data.items():
        station_name = vals.get("Nazwa stacji")
        if station_name:
            station_name = _with_spaces_to_snake(_remove_diacritics(station_name))
            result[key] = station_name
    return result

#e. Zweryfikuj, czy wszystkie stacje, których kod kończy się na „MOB” mają rodzaj stacji określony jako ‘mobilna’.
def verify_mob_stations(csv_data: Iterable) -> dict[str, bool]:
    _mob_code_re = re.compile(r"MOB$")

    stations_data = get_station_data(csv_data)
    result = {}
    for station_id, vals in stations_data.items():
        if re.search(_mob_code_re, station_id):
            rodzaj = vals.get("Rodzaj stacji", "")
            result[station_id] = rodzaj.strip().lower() == "mobilna"
    return result


#f. Wyodrębnij lokalizacje złożone z 3 członów rozdzielonych myślnikiem.
def get_three_part_locations(csv_data: Iterable) -> list[tuple[str, str, str, str]]:
    _three_part_dash_re = re.compile(r"^(?P<part1>[^-]+?) - (?P<part2>[^-]+?) - (?P<part3>[^-]+)$")

    stations_data = get_station_data(csv_data)
    result = []
    for station_id, vals in stations_data.items():
        name = vals.get("Nazwa stacji", "")
        match = re.match(_three_part_dash_re, name)
        if match:
            result.append(
                (
                    station_id,
                    match.group("part1"),
                    match.group("part2"),
                    match.group("part3"),
                )
            )
    return result

#g. Znajdź lokalizacje zawierające przecinek i nazwę ulicy (ul.) lub alei (al.)
def get_locations_with_comma_and_street(csv_data: Iterable) -> list[tuple[str, str]]:
    _street_with_comma_re = re.compile(r"(?:ul\.|al\.)[^,]*,|,[^,]*(?:ul\.|al\.)", re.IGNORECASE)

    stations_data = get_station_data(csv_data)
    result = []
    for station_id, vals in stations_data.items():
        address = vals.get("Adres", "")
        if address and re.search(_street_with_comma_re, address):
            result.append((station_id, address))
    return result