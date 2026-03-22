from get_data import Indexes
from collections import Counter

def get_most_active_session(log):
    if not log:
        return None
    counts = Counter(entry[Indexes.UID.value] for entry in log)
    uid, count = counts.most_common(1)[0]
    return uid, count