import sys

def get_line(input=sys.stdin):
    line = ''
    c = input.read(1) 
    
    while c != '\n':
        line += c
        c = input.read(1)
        if not c:
            raise EOFError
    
    return line

