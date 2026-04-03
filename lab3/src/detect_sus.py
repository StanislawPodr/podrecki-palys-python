from get_data import Indexes
from collections import defaultdict
def detect_sus(log, threshold=50, check_404=False, check_timing=False, timing_window_sec=1.0):

    ip_data = defaultdict(lambda: {'requests': [], 'codes': []})    #Dzielimy dane po ip
    for entry in log:
        ip = entry[Indexes.ID_ORIG_H.value]
        ip_data[ip]['requests'].append(entry[Indexes.TS.value])
        ip_data[ip]['codes'].append(entry[Indexes.STATUS_CODE.value])

    suspicious = []
    for ip, data in ip_data.items():
        total = len(data['requests'])
        if total < threshold:
            continue

        errors_404 = 0              #Czy wystarczająco 404
        for c in data['codes']:
            if c == 404: errors_404 += 1

        if check_404 and errors_404 < threshold // 2:
            continue

        min_interval = None         #Czy są za częste
        if check_timing:
            timestamps = sorted(data['requests'])
            intervals = [
                (timestamps[i+1] - timestamps[i]).total_seconds()
                for i in range(len(timestamps)-1)
            ]
            if intervals:
                min_interval = min(intervals)
                if min_interval >= timing_window_sec:
                    continue

        suspicious.append((ip, total, errors_404, min_interval))

    #Najwiecej requestow najbardziej podejrzane
    suspicious.sort(key=lambda x: x[1], reverse=True)
    return suspicious
