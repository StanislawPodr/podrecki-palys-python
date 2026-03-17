import sys

def get_line(input=sys.stdin):
    line = ''
    c = input.read(1) 
    
    while c != '\n':
        if not c:
            raise EOFError
        line += c
        c = input.read(1)
    
    return line

def get_sentence(input=sys.stdin):
    sentence = ""
    c = input.read(1)

    while c != '.':
        if not c:
            raise EOFError
        sentence += c
        c = input.read(1)
        
    return sentence

def get_next_word(iterator):
    word = ''
    try:
        chr = next(iterator)
        while chr.isspace():
            chr = next(iterator)
        
        while not chr.isspace():
            word += chr
            chr = next(iterator)
    except StopIteration:
        return word

    return word
