from get_data import Indexes

__HTTP_CODE_MIN = 100
__HTTP_CODE_MAX = 599

def get_entries_by_code(log, code):
    if code < __HTTP_CODE_MIN or code > __HTTP_CODE_MAX:
        raise ValueError('Wrong http code')
    return [data for data in log if data[Indexes.STATUS_CODE.value] == code]