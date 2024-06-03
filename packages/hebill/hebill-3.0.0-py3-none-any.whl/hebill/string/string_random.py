from .core import String
import string
import secrets


class StringRandom(String):
    def __new__(cls, length: int = 16):
        if length <= 0:
            raise ValueError("随机字符串长度必须为正整数")
        alphabet = string.ascii_letters + string.digits
        return str.__new__(cls, ''.join(secrets.choice(alphabet) for _ in range(length)))
