import sys
sys.stdin.reconfigure(encoding='utf-8') #polskie znaki
sys.stdout.reconfigure(encoding='utf-8')
from helper import get_sentence


def first_n_sentences(n, stream):
    count = 0
    try:
        while count < n:
            sentence = get_sentence(stream)
            yield sentence
            count += 1
    except EOFError:
        return

if __name__ == "__main__":
    for sentence in first_n_sentences(20, sys.stdin):
        print(sentence)