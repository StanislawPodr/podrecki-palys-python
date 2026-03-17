import sys
sys.stdin.reconfigure(encoding='utf-8') #polskie znaki
sys.stdout.reconfigure(encoding='utf-8')
from helper import get_sentence


def find_longest_sentence(stream=sys.stdin):
    longest = ""

    try:
        while True:
            sentence = get_sentence(stream)
            if len(sentence) > len(longest):
                longest = sentence
    except EOFError:
        return longest


if __name__ == "__main__":
    result = find_longest_sentence()
    print(result)