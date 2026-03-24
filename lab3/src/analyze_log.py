from get_data import Indexes
from collections import Counter
from count_by_method import count_by_method
from count_status_classes import count_status_classes
from get_most_active_session import get_most_active_session

def get_top_ips(log, n=10):
    counts = Counter(entry[Indexes.ID_ORIG_H.value] for entry in log)
    return counts.most_common(n)

def get_top_uris(log, n=10):
    counts = Counter(entry[Indexes.URI.value] for entry in log)
    return counts.most_common(n)

def get_failed_reads(log):
    errors_4xx = [e for e in log if 400 <= e[Indexes.STATUS_CODE.value] < 500]
    errors_5xx = [e for e in log if 500 <= e[Indexes.STATUS_CODE.value] < 600]

    return errors_4xx, errors_5xx


def analyze_log(log):
    if not log:
        return {
            'top_ips': [],
            'top_uris': [],
            'method_distribution': {},
            'status_classes': {},
            'error_count': 0,
            'unique_hosts': 0,
            'unique_clients': 0,
            'busiest_session': None,
            'time_range': None,
        }

    errors_4xx, errors_5xx = get_failed_reads(log)
    timestamps = [e[Indexes.TS.value] for e in log]

    return {
        'top_ips': get_top_ips(log, n=10),
        'top_uris': get_top_uris(log, n=10),
        'method_distribution': count_by_method(log),
        'error_count': len(errors_4xx) + len(errors_5xx),
        'most_active_session': get_most_active_session(log),
        'time_range': (min(timestamps), max(timestamps)),
    }