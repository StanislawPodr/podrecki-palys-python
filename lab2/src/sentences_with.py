import sys
from helper import get_sentence, get_next_word

# String ze słowami które powinny zawierać zdania
CONTAINS = 'i oraz ale że lub'
# Liczba wyrazów z powyższej listy kwalifikująca do zaliczenia zdania
MAX_NO = 2

def word_in_sequence(word, sequence):
    seq_it = iter(sequence)
    seq_element = get_next_word(seq_it)
    while seq_element and seq_element != word:
        seq_element = get_next_word(seq_it)
    return seq_element

def how_many_sentence_contain(sentence, words=CONTAINS):
    sentence_it = iter(sentence)
    result = 0

    word = get_next_word(sentence_it)
    found = ''
    while word:
        if word_in_sequence(word, words):
            found_before = word_in_sequence(word, found)
            if not found_before:
                found += word + ' '
                result += 1
        word = get_next_word(sentence_it)
    return result

def print_sentences(input=sys.stdin, output=sys.stdout, contains=CONTAINS, max_no=MAX_NO):
    while True:
        try:
            sentence = get_sentence(input)
            no_contained = how_many_sentence_contain(sentence.lower(), contains)
            if no_contained >= max_no:
                print(sentence + '\n', file=output, end='')
        except EOFError:
            break
    print()

if __name__ == "__main__":
    print_sentences()
