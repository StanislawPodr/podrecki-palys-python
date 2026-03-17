import sys
from helper import get_sentence

# Limit zdań podrzędnych w zdaniu
SUBORDINATE_NUMBER = 2

# Licznik zdań podrzędnych działający na zasadzie liczenia przecinków
def subordinate_counter(sentence):
    chrIdx = 0
    no_subordinate_clauses = 0
    while chrIdx < len(sentence):
        while chrIdx < len(sentence) and sentence[chrIdx] != ',':
            chrIdx += 1
        if chrIdx < len(sentence):
            no_subordinate_clauses += 1
            chrIdx += 1
    return no_subordinate_clauses

# Pierwsze zdanie z liczbą zdań podrzędnych większą niż limit
def get_fst_with_subordinates(input=sys.stdin, subordinate_number=SUBORDINATE_NUMBER):
    while True:
        try:
            sentence = get_sentence(input)
            if subordinate_counter(sentence) >= subordinate_number:
                return sentence + '\n'
        except EOFError:
            break
    return None

def print_fst_with_subordinates(input=sys.stdin, output=sys.stdout):
    print(get_fst_with_subordinates(input), file=output, end='')
    print()

if __name__ == "__main__":
    print_fst_with_subordinates()
