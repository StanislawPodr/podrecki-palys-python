from collections import Counter
from get_data import Indexes

def get_top_uris(logs, n=10):
    uris_counter = Counter([log[Indexes.URI.value] for log in logs])
    # Lista najczęściej używanych uri w formacie [(uri_1, liczba_użyć), ...]
    most_used_uris = uris_counter.most_common(n)
    # Funkcja zwraca tylko nazwę uri
    return [uri for uri, _ in most_used_uris]