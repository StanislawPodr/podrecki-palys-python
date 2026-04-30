import random
import string

class PasswordGenerator:
    DEFAULT_CHARSET = string.ascii_letters + string.digits
 
    def __init__(self, length: int = 7, charset: str = DEFAULT_CHARSET, count: int = 10):
        self.length  = length
        self.charset = charset
        self.count   = count
        self._generated = 0
 
    def __iter__(self):
        return self
 
    def __next__(self) -> str:
        if self._generated >= self.count:
            raise StopIteration
        password = "".join(random.choices(self.charset, k=self.length))
        self._generated += 1
        return password
 