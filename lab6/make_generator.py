import itertools

def make_generator(fun):
    for num in itertools.count(start=1):
        yield fun(num)

def fib(num):
    if num < 0:
        raise ValueError('num >= 0')
    fst = 0
    sec = 1
    for _ in range(num):
        nxt = fst + sec
        fst = sec
        sec = nxt
    return fst

if __name__ == "__main__":
    test_fib = make_generator(fib)
    print(list(itertools.islice(test_fib, 10)))
    test_aritm = make_generator(lambda x: x*1)
    print(list(itertools.islice(test_aritm, 10)))
    test_geom = make_generator(lambda x: 2**x)
    print(list(itertools.islice(test_geom, 10)))
