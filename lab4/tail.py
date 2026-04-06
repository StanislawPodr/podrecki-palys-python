import sys
import os
import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="program tail"
    )
    parser.add_argument(
        "--lines",
        type=int,
        default=10,
        metavar="n",
        help="liczba linii do wyświetlenia (deafult - 10)",
    )
    parser.add_argument(
        "--follow",
        action="store_true",
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="file path (opcjonalny)",
    )
    return parser.parse_args()


def read_last_lines(lines_iter, n):
    buffer = []
    for line in lines_iter:
        buffer.append(line)
        if len(buffer) > n:
            buffer.pop(0)
    return buffer

def print_lines(lines):
    for line in lines:
        print(line, end="")

def follow_file(path, n):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
        last = lines[-n:] if len(lines) >= n else lines
        print_lines(last)

        while True:
            line = f.readline()
            if line:
                print(line, end="", flush=True)
            else:
                time.sleep(0.1)


def main():
    args = parse_args()
    n = args.lines

    if args.file is not None:
        if not os.path.isfile(args.file):
            print(f"tail.py: {args.file}: Nie ma takiego pliku", file=sys.stderr)
            sys.exit(1)

        if args.follow:
            follow_file(args.file, n)
        else:
            with open(args.file, "r", encoding="utf-8", errors="replace") as f:
                last = read_last_lines(f, n)
            print_lines(last)

    else:
        if args.follow:
            print(
                "--follow nie dziala ze stdin",
                file=sys.stderr,
            )
            sys.exit(1)

        last = read_last_lines(sys.stdin, n)
        print_lines(last)


if __name__ == "__main__":
    main()