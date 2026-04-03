from get_data import Indexes
from collections import Counter
import re


def get_extension_stats(logs):
    file_extension_regex = re.compile(r'/\w+\.(\w+)($|\?)')
    uri_list = [log[Indexes.URI.value] for log in logs]
    extension_list = []
    for uri in uri_list:
        extension_got = re.search(file_extension_regex, uri)
        if extension_got:
            extension = extension_got.group(1)
            extension_list.append(extension)
    extension_counter = Counter(extension_list)
    return dict(extension_counter)


    