import sys
import io
sys.stdin.reconfigure(encoding='utf-8') #polskie znaki
sys.stdout.reconfigure(encoding='utf-8')
from helper import get_sentence, get_word

def has_no_adjacent_same_start(sentence):
    stream = io.StringIO(sentence)
    prev_letter = ""
    try:
        while True:
            word = get_word(stream)
            curr_letter = word[0].lower()
            if curr_letter == prev_letter:
                return False
            prev_letter = curr_letter
    except EOFError:
        return True

def longest_sentence_plus(stream=sys.stdin):
    longest = ""

    try:
        while True:
            sentence = get_sentence(stream)
            if has_no_adjacent_same_start(sentence):
                if len(sentence) > len(longest):
                    longest = sentence
    except EOFError:
        return longest


if __name__ == "__main__":
    result = longest_sentence_plus()
    print(result)