import sys
from helper import get_line

def count_chars(stream=sys.stdin):
    count = 0

    try:
        while True:
            line = get_line(stream)
            for ch in line:
                if ch != ' ' and ch != '\t' and ch != '\n' and ch != '\r': #Jezeli nie biały znak to +1
                    count += 1
    except EOFError:
        return count

if __name__ == "__main__":
    result = count_chars()
    print(result)