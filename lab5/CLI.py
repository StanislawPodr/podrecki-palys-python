import argparse
import logging
import random
import sys
from datetime import date, datetime
from pathlib import Path
from statistics import mean, stdev
from typing import Optional

from csv_parser import get_measurements_csv, get_station_data
from group_measurement_files_by_key import group_measurement_files_by_key

STATIONS_FILE = Path("stacje.csv")
MEASUREMENTS_DIR = Path("measurements")

VALID_QUANTITIES = {
    "PM2.5", "PM10", "NO", "NO2", "NOx", "SO2", "CO", "O3",
    "C6H6", "Pb(PM10)", "Cd(PM10)", "As(PM10)", "Ni(PM10)",
    "BaP(PM10)", "Hg",
}
VALID_FREQUENCIES = {"1g", "24g"}

logger = logging.getLogger(__name__)

def _setup_logging() -> None:
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda r: r.levelno < logging.ERROR)
    stdout_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(stdout_handler)
    root.addHandler(stderr_handler)

def _load_stations() -> dict:
    if not STATIONS_FILE.exists():
        logger.error("Plik stacji nie istnieje: %s", STATIONS_FILE)
        sys.exit(1)

    logger.info("Otwieranie pliku stacj: %s", STATIONS_FILE)
    with STATIONS_FILE.open("r", encoding="utf-8") as f:
        logger.info("Zamykanie pliku stacje: %s", STATIONS_FILE)
        data = get_station_data(f)

    if not data:
        logger.warning("Plik stacji jest pusty lub nieprawidłowy: %s", STATIONS_FILE)
    return data


def _load_measurements(path: Path) -> dict:
    if not path.exists():
        logger.error("Plik pomiarów nie istnieje: %s", path)
        sys.exit(1)

    logger.info("Otwieranie pliku pomiarów: %s", path)
    total_bytes = 0
    lines: list[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            total_bytes += len(line.encode("utf-8"))
            logger.debug("Przeczytano %d bajtów łącznie", total_bytes)
            lines.append(line)
    logger.info("Zamknięto plik pomiarów: %s (łącznie %d bajtów)", path, total_bytes)

    return get_measurements_csv(lines)


def _filter_by_date(measurements_data, start: date, end: date) -> list:
    values = []
    for m in measurements_data.measurements:
        if start <= m.date.date() <= end:
            try:
                values.append(float(m.result.replace(",", ".")))
            except (ValueError, AttributeError):
                pass
    return values


def _find_measurement_file(quantity: str, frequency: str, year: Optional[str] = None) -> Optional[Path]:
    files = group_measurement_files_by_key(MEASUREMENTS_DIR)
    candidates = [
        path
        for (y, q, f), path in files.items()
        if q == quantity and f == frequency and (year is None or y == year)
    ]
    if not candidates:
        return None
    return candidates[0]


def _cmd_random(args) -> None:
    start: date = args.start
    end: date = args.end
    quantity: str = args.quantity
    frequency: str = args.frequency

    meas_path = _find_measurement_file(quantity, frequency)
    if meas_path is None:
        logger.warning(
            "Brak pliku dla podanych paramterów.",
            quantity, frequency,
        )
        print("Brak pliku dla podanych paramterów.")
        return

    measurements = _load_measurements(meas_path)
    stations = _load_stations()

    active_station_ids = []
    for station_id, mdata in measurements.items():
        filtered = _filter_by_date(mdata, start, end)
        if filtered:
            active_station_ids.append(station_id)

    if not active_station_ids:
        logger.warning(
            "Brak stacji spełniających kryteria.",
            quantity, frequency, start, end,
        )
        print("Brak stacji spełniających kryteria.")
        return

    chosen_id = random.choice(active_station_ids)
    station_meta = stations.get(chosen_id, {})
    name = station_meta.get("Nazwa stacji", chosen_id)
    address = station_meta.get("Adres", "brak adresu")
    city = station_meta.get("Miejscowość", "")
    wojewodztwo = station_meta.get("Województwo", "")

    print(f"Losowa stacja mierząca {quantity} ({frequency}) w przedziale {start}–{end}:")
    print(f"  ID:        {chosen_id}")
    print(f"  Nazwa:     {name}")
    print(f"  Adres:     {address}, {city}, {wojewodztwo}")


def _cmd_stats(args) -> None:
    start: date = args.start
    end: date = args.end
    quantity: str = args.quantity
    frequency: str = args.frequency
    station_id: str = args.station_id

    meas_path = _find_measurement_file(quantity, frequency)
    if meas_path is None:
        logger.warning(
            "Brak pliku dla podanych parametrów.",
            quantity, frequency,
        )
        print("Brak pliku dla podanych parametrów.")
        return

    measurements = _load_measurements(meas_path)

    if station_id not in measurements:
        logger.warning(
            "Podana stacja nie istnieje.",
            station_id, quantity, frequency,
        )
        print(f"Podana stacja nie istnieje.")
        return

    values = _filter_by_date(measurements[station_id], start, end)

    if not values:
        logger.warning(
            "Brak pomiarów spełniających kryteria.",
            station_id, start, end,
        )
        print("Brak pomiarów spełniających kryteria.")
        return

    avg = mean(values)
    std = stdev(values) if len(values) > 1 else 0.0

    print(f"Statystyki: {quantity} ({frequency}), stacja {station_id}")
    print(f"  Przedział:          {start} – {end}")
    print(f"  Liczba pomiarów:    {len(values)}")
    print(f"  Średnia:            {avg:.4f}")
    print(f"  Odchylenie std:     {std:.4f}")


def _parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Podano złą datę")

def _parse_quantity(value: str) -> str:
    if value not in VALID_QUANTITIES:
        raise argparse.ArgumentTypeError(f"Podano złą wielkość")
    return value

def _parse_frequency(value: str) -> str:
    if value not in VALID_FREQUENCIES:
        raise argparse.ArgumentTypeError(f"Podano zły paramtetr")
    return value


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="air_quality",
        description=("Narzędzie do analizy danych ze stacji pomiarowych"),
    )

    parser.add_argument(
        "--quantity", "-q",
        required=True,
        type=_parse_quantity,
        metavar="WIELKOŚĆ",
        help="Mierzona wielkość (PM2.5, PM10, NO,... )",
    )
    parser.add_argument(
        "--frequency", "-f",
        required=True,
        type=_parse_frequency,
        metavar="CZĘSTOTLIWOŚĆ",
        help="Częstotliwość (1g/24g)",
    )
    parser.add_argument(
        "--start", "-s",
        required=True,
        type=_parse_date,
        metavar="RRRR-MM-DD",
        help="Początek przedziału czasowego (w formacie rrrr-mm-dd)",
    )
    parser.add_argument(
        "--end", "-e",
        required=True,
        type=_parse_date,
        metavar="RRRR-MM-DD",
        help="Koniec przedziału czasowego (w formacie rrrr-mm-dd)",
    )

    #Podkomendy
    subparsers = parser.add_subparsers(
        dest="command",
        metavar="PODKOMENDA",
        required=True,
    )

    subparsers.add_parser(
        "random",
        help="Nazwa i adres losowej stacji, która w zadanym przedziale czasowym mierzy tę wielkość.",
    )

    stats_parser = subparsers.add_parser(
        "stats",
        help="Obliczenie średniej i odchylenia standardowego danej wielkości w zadanym przedziale czasowym dla danej stacji",
    )

    stats_parser.add_argument(
        "station_id",
        metavar="ID_STACJI",
        help="Kod stacji",
    )

    return parser
