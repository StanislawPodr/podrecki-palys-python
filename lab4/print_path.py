#!/usr/bin/python3

import os
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        prog="print_path", description="Prints PATH variable elements"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print all executable files in PATH",
    )
    return parser


def get_executables(directory: Path):
    return [
        executable
        for executable in directory.iterdir()
        if executable.is_file() and os.access(executable, os.X_OK)
    ]


def print_path():
    parser = parse_args()
    args = parser.parse_args()
    is_verbose = args.verbose

    path_var = os.environ["PATH"]
    # W zmiennej PATH ścieżki są rozdzielane ":"
    paths_str = path_var.split(":")
    paths = [Path(path) for path in paths_str]

    if is_verbose:
        for path in paths:
            if path.is_dir():
                execs = get_executables(path)
                for executable in execs:
                    print(executable)
    else:
        for path in paths:
            if path.is_dir():
                print(path)


if __name__ == "__main__":
    print_path()
