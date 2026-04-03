from get_data import Indexes

def count_by_method(log):
    counts = {}
    for entry in log:
        method = entry[Indexes.METHOD.value]
        counts[method] = counts.get(method, 0) + 1
    return counts