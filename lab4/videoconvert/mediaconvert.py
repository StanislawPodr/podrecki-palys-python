#!/usr/bin/python3

import sys
import subprocess
import argparse
from utilis import check_input_file, check_output_file, get_path_to_output
from videoconvert import get_ffmpeg_formats, cvt_using_ffmpeg

def get_parser(formats: dict[str, set[str]]):
    parser = argparse.ArgumentParser(
        prog="mediaconvert", description="Converts media between formats",
        epilog=f"Suported formats: {formats}"
    )

    parser.add_argument(
        "path",
        help="path to input file",
        type=check_input_file(formats['decodable'])
    )

    parser.add_argument(
        "format",
        help="output file format",
        type=check_output_file(formats['encodable'])
    )
    return parser

def main():
    try:
        formats = get_ffmpeg_formats()
        parser = get_parser(formats).parse_args()

        input_path = parser.path
        output_format = parser.format
        output_path = get_path_to_output(output_format, input_path)

        # Utworzenie katalogu dla outputu
        output_path.parent.mkdir(parents=True, exist_ok=True)

        result = cvt_using_ffmpeg(input_path, output_path).stdout 
        if result:
            print(result.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print("stderr:", e.stderr, file=sys.stderr)
        sys.exit(e.returncode)
    except OSError:
        print("Failed to create target. Check permissions.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
