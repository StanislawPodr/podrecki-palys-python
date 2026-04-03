import subprocess
import re
from pathlib import Path

# Po tej linii zaczyna się lista formatów
FORMAT_LIST_START = ' --'

def cvt_using_ffmpeg(input_file: Path, result_file: Path) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ['ffmpeg', '-y', '-i', str(input_file), str(result_file)],
        check=True,
        capture_output=True
    )
    return result


def get_ffmpeg_formats() -> set[str, list[str]]:
    result = subprocess.run(
        ['ffmpeg', '-formats'],
        check=True,
        capture_output=True
    )
    ouput_utf8 = result.stdout.decode("utf-8")

    lines = ouput_utf8.splitlines()
    lines_iter = iter(lines)

    while next(lines_iter) != FORMAT_LIST_START:
        pass

    # Output ffmpeg -formats zwraca listę kodeków w formacie, gdzie DE oznaczają Demuxing i Muxing
    decodable_pattern = re.compile(r'^ D[E ] (?P<format>[\w,]+)')
    encodable_pattern = re.compile(r'^ [D ]E (?P<format>[\w,]+)')
    decodable = set()
    encodable = set()

    for line in lines_iter:
        decodable_match = re.search(decodable_pattern, line)
        encodable_match = re.search(encodable_pattern, line)

        if decodable_match:
            formats = decodable_match.group('format')
            for format_ in formats.split(','):
                decodable.add(format_)

        if encodable_match:
            formats = encodable_match.group('format')
            for format_ in formats.split(','):
                encodable.add(format_)

    return {"decodable": decodable, "encodable": encodable}
