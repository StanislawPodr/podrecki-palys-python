from get_data import Indexes

def get_unique_methods(log):
    methods = set()
    for entry in log:
        method = entry[Indexes.METHOD.value]
        methods.add(method)
    return list(methods)