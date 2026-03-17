import sys
sys.stdin.reconfigure(encoding='utf-8') #polskie znaki
def paragraph_count(stream=sys.stdin):
    count = 0
    is_paragraph_new = True

    for line in stream:
        if (line.strip() == ""): #Zmiana flagi jesli pusta linijka
            is_paragraph_new = True
        else:
            if is_paragraph_new: #Jezeli ostatnia linia byla pusta to +1 paragraf
                count += 1
            is_paragraph_new = False
    return count

if __name__ == "__main__":
    result = paragraph_count(sys.stdin)
    print(result)