from get_data import Indexes

def count_status_classes(log):

    classes = {'2xx': 0, '3xx': 0, '4xx': 0, '5xx': 0}
    for entry in log:
        code = entry[Indexes.STATUS_CODE.value]
        if code is not None:
            prefix = str(code//100) + "xx"
            if prefix in classes:
                classes[prefix] += 1
    return classes