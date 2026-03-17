import sys
from helper import get_line

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# maksymalna liczba linii preambuły
MAX_HEADER_LINES = 10
# liczba pustych linii oddzielająca preambułę
LINES_DIVIDING_PREAMBLE = 2


def echo(sentence):
    return "("+sentence+")"


def skip_book_preamble(stream=sys.stdin, max_header_lines=MAX_HEADER_LINES, 
                       lines_dividing_preamble=LINES_DIVIDING_PREAMBLE):
    lines_counter = 0
    last_empty_lines = 0

    prev_was_new_line = True
    c = stream.read(1)
    while c and lines_counter < max_header_lines and last_empty_lines < lines_dividing_preamble:
        if c == '\n':
            lines_counter += 1
            if prev_was_new_line:
                last_empty_lines += 1
            prev_was_new_line = True
        else:
            prev_was_new_line = False
        c = stream.read(1)

def remove_additional_spaces(line):
    output = ''
    prev_was_space = False
    for chr in line:
        curr_is_space = (chr == ' ')
        if not curr_is_space or not prev_was_space:
            output += chr
        prev_was_space = curr_is_space
    return output


def print_book_fixed(input=sys.stdin, output=sys.stdout):
    try:
        # Usuwanie pustych linii z przodu
        line = get_line(input).strip()
        while not line:
            line = get_line(input).strip()

        # wypisanie wszystkich linii z usunięciem spacji i znaków białych z przodu i z tyłu
        while True:
            print(remove_additional_spaces(line), file=output) 
            line = get_line(input).strip()
    except EOFError: 
        return    


def main():
    skip_book_preamble()
    print_book_fixed()


if __name__ == "__main__":
    main()
