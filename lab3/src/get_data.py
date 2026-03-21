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
        datetime.fromtimestamp(int(data[__AllIndexes.TS])),
        data[__AllIndexes.UID],
        data[__AllIndexes.ID_ORIG_H],
        int(data[__AllIndexes.ID_ORIG_P]),
        data[__AllIndexes.ID_RESP_H],
        int(data[__AllIndexes.ID_RESP_P]),
        data[__AllIndexes.METHOD],
        data[__AllIndexes.HOST],
        data[__AllIndexes.URI],
        int(data[__AllIndexes.STATUS_CODE])
    )

def entry_to_dict(enter):
    ts, uid, id_orig_h, id_orig_p, id_resp_h, id_resp_p, method, host, uri, status_code = enter
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
        'status_code': status_code
    }

def validate_data_tuple(data):
    for info in data:
        if info in '-':
            raise ValueError('The value is not set')
    return data

def convert_data_dict(data_dict):
    # Istniejące dane, które można konwertować powinny zostać przekonwertowane
    # TODO może się kiedyś przydać i dodać do returna w get_data_dict
    pass


def get_data_dict(line):
    # Dane są separowane tabulatorem, "-" oznacza brak wartości, więc nie bierzemy go do słownika
    data = zip(LOG_KEYS, line.split('\t'))
    return {k: v for (k, v) in data if not v in '-'}

# Zwraca listę tupleów z danymi z stdin
def read_log():
    list_of_tuples = []
    while True:
        try:
            line = input().strip()
            if line:
                data_tuple = validate_data_tuple(get_data_tuple(line))
                list_of_tuples.append(data_tuple)
        except EOFError:
            break
        except:
            pass # Skipujemy wybrakowane rekordy 
    return list_of_tuples
