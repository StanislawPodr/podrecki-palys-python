from collections import defaultdict
from functools import reduce
import itertools

#1a
def acronym(words):
    return reduce(lambda acc, w: acc + w[0].upper(), words, "")

#1b
# Przekomplikowany algorytm szukania mediany. Nie działa dla [], ale nie ma ifów
def median(numbers_list: list):
    numbers_sorted = sorted(numbers_list)
    mid_sec = len(numbers_sorted) // 2
    mid_fst = mid_sec - (len(numbers_sorted) + 1) % 2
    return (numbers_sorted[mid_fst] + numbers_sorted[mid_sec]) / 2

#1c
def flatten(lst):
    def flatten_element(element):
        # Operator ternarny: jeśli element jest listą lub krotką – rekurencja
        return flatten(list(element)) if isinstance(element, (list, tuple)) else [element]
 
    return reduce(lambda acc, el: acc + flatten_element(el), lst, [])
#1d
def make_alpha_dict(alpha: str):
    alpha_list_sorted = sorted(alpha.split())
    grouped_by_fst_letter = itertools.groupby(alpha_list_sorted, lambda word: word[:1])
    return {key: list(iterator) for key, iterator in grouped_by_fst_letter}

# Trochę słabo z tym funkcyjnym podejściem jak nie ma niemutowalnych struktur danych
def group_anagrams(word_list: list[str]):
    anagrams = defaultdict(list)
    def group_anagrams_rec(left: list[str]):
        match left:
            case [hd, *tl]:
                anagrams[''.join(sorted(hd))].append(hd)
                group_anagrams_rec(tl)
            case _:
                return
    group_anagrams_rec(word_list)
    return dict(anagrams)
