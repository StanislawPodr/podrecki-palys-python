import csv
from collections import namedtuple
from typing import Iterable, Iterator
from datetime import datetime

from measurements_data import Measurement, MeasurementsData


# Format daty i godziny stosowany w plikach csv. Np. "%d/%m/%y %H:%M"
_DATETIME_FORMAT = "%d/%m/%y %H:%M"

# Informacje zawarte w headerze pliku z danymi csv
_MeasurementsHdr = namedtuple(
    "Measurements", ["station_id", "type", "measurement_time", "unit", "job_name"]
)


def _get_header_data_csv(csv_iterator: Iterator):
    try:
        # Parsowanie headera. Pierwsza kolumna to zawsze klucz po polsku, który pomijamy
        # Pierwsza linia to niepotrzebne, lokalne indeksy które pomijamy
        next(csv_iterator)
        # Druga linia to unikalne identyfikatory stacji np. DsOsieczow21
        [_, *station_ids] = next(csv_iterator)
        # Trzecia to wskaźniki np. Cd(PM10)
        [_, *types] = next(csv_iterator)
        # Czwarta to czasy uśredniania np. 24h
        [_, *times] = next(csv_iterator)
        # Piąta to jednostka pomiaru np. ng/m3
        [_, *units] = next(csv_iterator)
        # Szósta to kod stanowiska
        [_, *job_names] = next(csv_iterator)
    except (StopIteration, ValueError):
        return []

    return [
        _MeasurementsHdr(station_id, type, time, unit, job)
        for station_id, type, time, unit, job in zip(
            station_ids, types, times, units, job_names
        )
    ]

def get_measurements_csv(csv_data: Iterable[str]):
    csv_reader = csv.reader(csv_data)
    csv_iterator = iter(csv_reader)
    hdr_data = _get_header_data_csv(csv_iterator)
    result = {
        station_id: MeasurementsData(type, time, unit, job, [])
        for station_id, type, time, unit, job in hdr_data
    }
    for [date_and_time, *results] in csv_iterator:
        datetime_format = datetime.strptime(date_and_time, _DATETIME_FORMAT)
        for (station_id, *_), measurement_result in zip(hdr_data, results):
            result[station_id].measurements.append(
                Measurement(datetime_format, measurement_result)
            )
    return result

def get_station_data(csv_data: Iterable[str]):
    csv_reader = csv.reader(csv_data)
    csv_iterator = iter(csv_reader)
    try:
        header = next(csv_iterator)
        if len(header) < 2:
            return {}
        [_, _, *keys] = header
    except (StopIteration, ValueError):
        return {}
    result = {}
    for row in csv_iterator:
        if len(row) < 2:
            continue
        [_, station_id, *data] = row
        result[station_id] = dict(zip(keys, data))
    return result
