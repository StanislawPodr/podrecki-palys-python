import sys
import io
sys.stdin.reconfigure(encoding='utf-8') #polskie znaki
sys.stdout.reconfigure(encoding='utf-8')
from helper import get_sentence, get_word


def count_words(sentence):
    stream = io.StringIO(sentence)
    count = 0
    try:
        while True:
            get_word(stream)
            count += 1
    except EOFError:
        return count


def sentences_under5(stream):
    try:
        while True:
            sentence = get_sentence(stream)
            if count_words(sentence) <= 4:
                yield sentence
    except EOFError:
        return


if __name__ == "__main__":
    for sentence in sentences_under5(sys.stdin):
        print(sentence)