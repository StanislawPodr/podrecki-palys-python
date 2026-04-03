from get_data import read_log
from sort_log import sort_log
from get_entries_by_addr import get_entries_by_addr
from get_entries_by_extension import get_entries_by_extension
from unique_methods import  get_unique_methods
from count_by_method import count_by_method
from count_status_classes import count_status_classes
from entry_to_dict import entry_to_dict
from entry_to_dict import log_to_dict
from get_most_active_session import get_most_active_session
from detect_sus import detect_sus
from get_failed_reads import get_failed_reads

log = read_log()

#print(sort_log(log, index=0))
#print(get_entries_by_addr(log, "192.168.202.79"))
#print(get_entries_by_extension(log, "jpg"))
#print(get_unique_methods(log))
#print(count_by_method(log))
#print(count_status_classes(log))

#for uid, entries in log_dict.items():
#    if(len(entries) != 1):
#        print(f"Sesja {uid}: {len(entries)} wpisy")

#print(get_most_active_session(log))
#print (detect_sus(log))

print(get_failed_reads(log))
