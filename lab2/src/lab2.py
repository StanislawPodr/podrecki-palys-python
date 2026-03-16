import sys
def echo(sentence):
    return "("+sentence+")"

def main(process_sentence):
    sentence = ""
    c = sys.stdin.read(1)

    while c:
        sentence += c
        if c in ".":
            print(process_sentence(sentence.strip()))
            sentence = ""
        c = sys.stdin.read(1)

if __name__ == "__main__":
    main(echo)
