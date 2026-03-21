from collections import Counter
from get_data import Indexes

def get_top_ips(logs, n=10):
    # Krotki z adresem źródłowym i docelowym
    ip_tuples = [(log[Indexes.ID_ORIG_H], log[Indexes.ID_RESP_H]) for log in logs]
    # Żeby policzć każdy adres trzeba je "spłaszczyć"
    ips = [ip for ip_tuple in ip_tuples for ip in ip_tuple]
    count = Counter(ips)
    return count.most_common(n)