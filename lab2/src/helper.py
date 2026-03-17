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
    is_last_nl = False

    while True:
        c = input.read(1)

        if not c:
            if sentence.strip():
                return sentence.strip()
            raise EOFError

        if c == "\n":
            if is_last_nl:  # nowy akapit - zwroc zdanie jesli jest
                if sentence.strip():
                    return sentence.strip()
                is_last_nl = False
                sentence = ""
            else:
                is_last_nl = True
                sentence += " "  # zdanie dalej w nowej lini
        else:
            is_last_nl = False
            if c in ".!?:":
                return sentence.strip()
            sentence += c

def get_word(stream):
    c = stream.read(1)
    while c and not c.isalpha():  # dopoki nie litera - kolejny znak
        c = stream.read(1)
    if not c:
        raise EOFError

    word = ""
    while c and c.isalpha():
        word += c
        c = stream.read(1)
    return word

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
