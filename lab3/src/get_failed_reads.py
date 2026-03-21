from get_data import Indexes

def get_failed_reads(log, merge=False):
    status_400 = []
    status_500 = []
    for data in log:
        status_code = data[Indexes.STATUS_CODE] 
        if 400 <= status_code < 500:
            status_400.append(data)
        elif 500 <= status_code < 600:
            status_500.append(data)
    if merge:
        return status_400 + status_500
    return (status_400, status_500)
