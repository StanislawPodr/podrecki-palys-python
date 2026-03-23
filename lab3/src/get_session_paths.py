from get_data import log_to_dict


def get_session_path(logs):
    log_dict = log_to_dict(logs)
    # Zwraca niepowtarzające się uri dla każdej sesji
    return {uid: list(set([request['uri'] for request in session])) for uid, session in log_dict.items()}
