def sort_log(log, index):
    if not log:
        return []

    max_index = len(log[0]) - 1
    if index < 0 or index > max_index:
        raise IndexError()

    return sorted(log, key=lambda entry: entry[index])
