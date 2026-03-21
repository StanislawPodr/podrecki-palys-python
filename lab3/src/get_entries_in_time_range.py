from get_data import Indexes

def get_entries_in_time_range(logs, start, end):
    if start > end:
        raise ValueError("Start timestamp should be lower than end timestamp")
    return [log for log in logs if start <= log[Indexes.TS] < end]