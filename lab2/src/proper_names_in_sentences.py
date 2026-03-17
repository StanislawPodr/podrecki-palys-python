import sys
from helper import get_sentence

def has_proper_name(sentence):
    chrIdx = 0
    # pomijamy pierwszy wyraz
    while chrIdx < len(sentence) and sentence[chrIdx].isspace(): 
        chrIdx += 1
    while chrIdx < len(sentence) and not sentence[chrIdx].isspace():
        chrIdx += 1
    
    # szukamy wyrazu zaczynającego się od wielkiej litery
    while chrIdx < len(sentence):
        while chrIdx < len(sentence) and sentence[chrIdx].isspace(): 
            chrIdx += 1
        if chrIdx < len(sentence) and sentence[chrIdx].isupper():
            return True
        while chrIdx < len(sentence) and not sentence[chrIdx].isspace():
            chrIdx += 1
    return False

def get_proper_names(input=sys.stdin):
    with_proper_names = 0
    no_sentences = 0
    while True:
        try:
            sentence = get_sentence(input)
            # Zdanie może być puste, wtedy nie bierzemy go pod uwagę
            if sentence:
                if has_proper_name(sentence):
                    with_proper_names += 1
                no_sentences += 1
        except EOFError:
            break
    
    if no_sentences == 0:
        return 1

    return with_proper_names / no_sentences

def print_ratio(input=sys.stdin, output=sys.stdout):
    print(get_proper_names(input), file=output) 

if __name__ == "__main__":
    print_ratio()
