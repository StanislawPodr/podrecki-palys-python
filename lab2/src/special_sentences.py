import sys
from helper import get_sentence
sys.stdin.reconfigure(encoding='utf-8') #polskie znaki

def is_question_or_exclamation(sentence):
    last = ""
    for ch in sentence:
        if ch.strip():
            last = ch
    return last == "?" or last == "!"


def special_sentences(stream=sys.stdin):
    try:
        while True:
            sentence = get_sentence(stream)
            if is_question_or_exclamation(sentence):
                yield sentence
    except EOFError:
        return


if __name__ == "__main__":
    for sentence in special_sentences():
        print(sentence)