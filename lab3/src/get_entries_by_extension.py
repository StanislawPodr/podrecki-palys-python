from get_data import Indexes

def get_entries_by_extension(log, ext):
    if not isinstance(ext, str) or not ext.strip():
        raise ValueError()

    ext = ext.lstrip('.').lower()

    result = []
    for entry in log:
        uri = entry[Indexes.URI.value]
        path = uri.split('?')[0]    #Tekst tylko przed "?"
        dot_pos = path.find('.')
        if dot_pos != -1:           #Porównujemy tekst za "." jeśli jest
            file_ext = path[dot_pos + 1:].lower()
            if file_ext == ext:
                result.append(entry)
    return result