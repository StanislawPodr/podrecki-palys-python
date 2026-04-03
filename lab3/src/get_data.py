from datetime import datetime
from enum import Enum, auto

LOG_KEYS = [
    'ts', 'uid', 'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'trans_depth',
    'method', 'host', 'uri', 'referrer', 'user_agent', 'request_ body_len', 'response_ body_len',
    'status_code', 'status_msg', 'info_code', 'info_msg', 'filename', 'tags', 'username',
    'password', 'proxied', 'orig_fuids', 'orig_mime_types', 'resp_fuids', 'resp_mime_types'
]

class __AllIndexes(Enum):  
    TS = 0
    UID = auto()
    ID_ORIG_H = auto()
    ID_ORIG_P = auto()
    ID_RESP_H = auto()
    ID_RESP_P = auto()
    TRANS_DEPTH = auto()
    METHOD = auto()
    HOST = auto()
    URI = auto()
    REFERRER = auto()
    USER_AGENT = auto()
    REQUEST_BODY_LEN = auto()
    RESPONSE_BODY_LEN = auto()
    STATUS_CODE = auto()
    STATUS_MSG = auto()
    INFO_CODE = auto()
    INFO_MSG = auto()
    FILENAME = auto()
    TAGS = auto()
    USERNAME = auto()
    PASSWORD = auto()
    PROXIED = auto()
    ORIG_FUIDS = auto()
    ORIG_MIME_TYPES = auto()
    RESP_FUIDS = auto()
    RESP_MIME_TYPES = auto()

class Indexes(Enum):
    TS = 0
    UID = auto()
    ID_ORIG_H = auto()
    ID_ORIG_P = auto()
    ID_RESP_H = auto()
    ID_RESP_P = auto()
    METHOD = auto()
    HOST = auto()
    URI = auto()
    STATUS_CODE = auto()

# Zwraca tuple z linii
def get_data_tuple(line):
    data = line.split('\t')
    return (
        datetime.fromtimestamp(float(data[__AllIndexes.TS.value])),
        data[__AllIndexes.UID.value],
        data[__AllIndexes.ID_ORIG_H.value],
        int(data[__AllIndexes.ID_ORIG_P.value]),
        data[__AllIndexes.ID_RESP_H.value],
        int(data[__AllIndexes.ID_RESP_P.value]),
        data[__AllIndexes.METHOD.value],
        data[__AllIndexes.HOST.value],
        data[__AllIndexes.URI.value],
        correct_int(data[__AllIndexes.STATUS_CODE.value])
    )#Dodałem .value bo cos nie dzialalo

def correct_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def validate_data_tuple(data):
    for info in data:
        if info in '-':
          raise ValueError('The value is not set')
    return data

# Zwraca listę tupleów z danymi z stdin
def read_log():
    list_of_tuples = []
    while True:
        try:
            line = input().strip()
            if line:
                data_tuple = get_data_tuple(line)   #bez validate bo na razie nie dzialalo
                list_of_tuples.append(data_tuple)
        except EOFError:
            break
        except Exception as e:
            import sys
            print(f"BŁĄD: {e}", file=sys.stderr)
    return list_of_tuples

from collections import defaultdict

def entry_to_dict(entry):
    ts, uid, id_orig_h, id_orig_p, id_resp_h, id_resp_p, method, host, uri, status_code = entry
    return {
        'ts': ts,
        'uid': uid,
        'id.orig_h': id_orig_h,
        'id.orig_p': id_orig_p,
        'id.resp_h': id_resp_h,
        'id.resp_p': id_resp_p,
        'method': method,
        'host': host,
        'uri': uri,
        'status_code': status_code,
    }

def log_to_dict(log):
    result = defaultdict(list)
    for entry in log:
        uid = entry[Indexes.UID.value]
        result[uid].append(entry_to_dict(entry))
    return dict(result)
