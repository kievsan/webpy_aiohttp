from hashlib import md5


def md5_hash_password(password: str) -> str:
    # преобразуем в байты
    password: bytes = password.encode()
    # байты положили в md5, привели к строке
    hashed_password = md5(password).hexdigest()
    return hashed_password