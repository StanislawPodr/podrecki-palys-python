import sys
import os
import json
import subprocess
from collections import Counter


DEFAULT_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wc_json.sh")
ANALYZE_SCRIPT = os.environ.get("ANALYZE_SCRIPT", DEFAULT_SCRIPT)

def to_bash_path(path: str) -> str:
    path = os.path.abspath(path).replace("\\", "/")
    if len(path) >= 2 and path[1] == ":":
        path = f"/{path[0].lower()}{path[2:]}"
    return path


def find_text_files(directory: str) -> list[str]:
    text_files = []
    for root, _dirs, files in os.walk(directory):
        for name in sorted(files):
            if not name.endswith(".txt"):
               continue
            path = os.path.join(root, name)
            try:
                with open(path, "r", encoding="utf-8", errors="strict") as f:
                    f.read(512)
                text_files.append(path)
            except (UnicodeDecodeError, PermissionError):
                pass
    return text_files


def analyze_file(bash: str, bash_script: str, path: str) -> dict | None:
    try:
        result = subprocess.run(
            [bash, bash_script],
            input=to_bash_path(path),
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        print(f"Nie znaleziono skryptu: {bash_script}", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"TimeoutExpired: {path}", file=sys.stderr)
        return None

    raw = result.stdout.strip()
    if not raw:
        stderr_info = result.stderr.strip()
        print(f"  BŁĄD ({path}): brak outputu" + (f" – {stderr_info}" if stderr_info else ""), file=sys.stderr)
        return None

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  błąd parsowania ({path}): {e}", file=sys.stderr)
        print(f"  Raw output: {raw[:300]}", file=sys.stderr)
        return None

    return {
        "path":             data.get("file", path),
        "chars":            int(data.get("noChars", 0)),
        "words":            int(data.get("noWords", 0)),
        "lines":            int(data.get("noLines", 0)),
        "most_common_char": data.get("mostUsedChar", ""),
        "most_common_word": data.get("mostUsedWord", ""),
    }

def print_summary(results: list[dict]) -> None:
    total_chars = sum(r["chars"] for r in results)
    total_words = sum(r["words"] for r in results)
    total_lines = sum(r["lines"] for r in results)

    char_counter: Counter = Counter()
    word_counter: Counter = Counter()
    for r in results:
        if r["most_common_char"]:
            char_counter[r["most_common_char"]] += r["chars"]
        if r["most_common_word"]:
            word_counter[r["most_common_word"]] += r["words"]

    global_char = char_counter.most_common(1)[0][0] if char_counter else "–"
    global_word = word_counter.most_common(1)[0][0] if word_counter else "–"

    print("\nPODSUMOWANIE\n")
    print(f"Liczba przeanalizowanych plików : {len(results)}")
    print(f"Ilość znaków        : {total_chars}")
    print(f"Ilość słów          : {total_words}")
    print(f"Ilość wierszy       : {total_lines}")
    print(f"Najczęstszy znak    : {repr(global_char)}")
    print(f"Najczęstsze słowo   : {global_word}")


def main():
    if len(sys.argv) < 2:
        print("podaj sciezke do katalogu", file=sys.stderr)
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("podany argument nie jest katalogiem", file=sys.stderr)
        sys.exit(1)


    bash = "bash"
    bash_script = to_bash_path(ANALYZE_SCRIPT)

    print(f"katalog     : {os.path.abspath(directory)}")

    files = find_text_files(directory)

    if not files:
        print("nie znaleziono zadnych plikow")
        sys.exit(0)

    print(f"znaleziono {len(files)} plików.\n")

    results: list[dict] = []
    for path in files:
        print(f"  analizuję: {path}")
        data = analyze_file(bash, bash_script, path)
        if data:
            results.append(data)

    if not results:
        print("brak wynikow")
        sys.exit(0)

    print_summary(results)


if __name__ == "__main__":
    main()