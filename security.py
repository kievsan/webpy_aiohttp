from hashlib import md5

from bcrypt import hashpw, checkpw, gensalt


def md5_hash_password(password: str) -> str:
    # преобразуем в байты
    password: bytes = password.encode()
    # байты положили в md5, привели к строке
    hashed_password = md5(password).hexdigest()
    return hashed_password


def bcrypt_hash_password(password: str) -> str:
    password: bytes = password.encode()
    password = hashpw(password=password, salt=gensalt())
    password: str = password.decode()
    return password