from get_data import Indexes

def _is_valid_ip(addr):
    parts = addr.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        if not 0 <= int(part) <= 255:
            return False
    return True

def get_entries_by_addr(log, addr):

    if not isinstance(addr, str) or not addr.strip():
        raise ValueError()

    addr = addr.strip()

    if not _is_valid_ip(addr):
        raise ValueError()

    return [
        entry for entry in log
        if entry[Indexes.ID_ORIG_H.value] == addr or entry[Indexes.HOST.value] == addr
    ]