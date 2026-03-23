import sys
sys.path.insert(0, "./src")






if __name__ == "__main__":
    from get_data import read_log, Indexes
    logs = read_log()

    print('test get_entries_by_code') 
    from get_entries_by_code import get_entries_by_code
    print(get_entries_by_code(logs, 200))

    print('test get_failed_reads') 
    from get_failed_reads import get_failed_reads
    print(get_failed_reads(logs, True))

    print('test get_top_ips')
    from get_top_ips import get_top_ips
    print(get_top_ips(logs))

    print('test get_entries_in_time_range') 
    from get_entries_in_time_range import get_entries_in_time_range
    from datetime import datetime
    start = datetime.fromtimestamp(1331901000.000000)
    end = datetime.fromtimestamp(1331901001.000000)
    print(get_entries_in_time_range(logs, start, end))

    print('test get_top_uris') 
    from get_top_uris import get_top_uris
    print(get_top_uris(logs))

    print('test entry_to_dict') 
    from get_data import entry_to_dict, log_to_dict
    print(entry_to_dict(logs[0]))

    logs_dict = log_to_dict(logs)

    print('test print_dict_entry_dates')
    from print_dict_entry_dates import print_dict_entry_dates
    print_dict_entry_dates(logs_dict)

    print('test get_session_paths')
    from get_session_paths import get_session_path
    print(get_session_path(logs))

    print('test get_extension_stats')
    from get_extension_stats import get_extension_stats
    print(get_extension_stats(logs))
