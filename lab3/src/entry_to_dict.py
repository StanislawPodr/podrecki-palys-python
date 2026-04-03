from collections import defaultdict
from get_data import Indexes

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

