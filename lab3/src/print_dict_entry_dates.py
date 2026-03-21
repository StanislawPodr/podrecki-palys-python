from collections import Counter
from functools import reduce

def print_dict_entry_dates(log_dict):
    for uid, session in log_dict.items():
        print(f'Session UID: {uid}')
        print(f'First request date: {session[0]['ts']}')
        print(f'Last request date: {session[-1]['ts']}')
        print(f'Number of requests: {len(session)}')
        # Wynikiem jest lista tupleów z ip źródłowym i docelowym dla zapytania
        session_ips = [(req['id.orig_h'], req['id.resp_h']) for req in session]
        # Adresy są rozłożone z krotki i wrzucone do zbioru bez powtórzeń
        hosts = set([ip for ip_tuple in session_ips for ip in ip_tuple])
        print(f'Hosts in session: {hosts}')
        # Udział metod HTTP
        http_methods = Counter([request['method'] for request in session])
        counted = http_methods.most_common()
        methods_usage_proportion = [(name, used / len(counted)) for name, used in counted]
        print(f'Method usage proportion: {methods_usage_proportion}')
        # Stosunek liczby kodów 200
        add_200_code = lambda acc, code: acc + 1 if 200 <= code < 300 else acc
        code_list = [request['status_code'] for request in session]
        no_200_codes = reduce(add_200_code, code_list, 0)
        print(f'Proportion of 200 codes: {no_200_codes / len(code_list)}')
        print()
