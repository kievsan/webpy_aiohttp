import pydantic     # содержит СХЕМЫ ВАЛИДАЦИИ

import requests as requests

from typing import Optional


URL = f'http://localhost:5000/user/'

def password_min_lenght(min_lenght = 8):
    msg = f"passwortd short: length less than {min_lenght} signs!"
    return min_lenght, msg


class CreateUser(pydantic.BaseModel):   # здесь будет валидация пользователя
                                        # (того, что пойдет в post)
    username: str       # два обязательных поля:
    password: str       # то, что должен прислать клиент!
    email: Optional[str] = 'missing@email'

    # Можно добавить валидации, напр, проверять сложность пароля

    @pydantic.field_validator('password')
    def validate_password(cls, value):
        # cls               -   класс, value - значение
        # password          -   валидируемое поле
        # validate_password -   так можем давать название методам валидации
        min_len, msg = password_min_lenght()
        if len(value) < min_len:
            # нужно выбросить исключение именно ValueError,
            # и библ. pydantic его правльно обработает!
            raise ValueError(msg)
        # возвращаем уже валидированное значение
        # (иногда здесь хешируют пароль, но лучше делать отдельно!)
        return value


class PatchUser(pydantic.BaseModel):
    username: Optional[str] = None          # поля опциональны
    password: Optional[str] = None          # (не обязательно все обновлять...)
    email: Optional[str] = None

    @pydantic.field_validator('password')
    def validate_password(cls, value):
        min_len, msg = password_min_lenght()
        if len(value) < min_len:
            raise ValueError(msg)
        return value


class CreateAd(pydantic.BaseModel):   # валидация новой рекламы

    user_id: int
    header: Optional[str] = 'made ad'
    description: Optional[str] = None

    @pydantic.field_validator('user_id')
    async def validate_ad_owner(cls, value):
        response = requests.get(URL + value)
        if response.status_code != 200:
            raise ValueError('user not found...')
        return value


class PatchAd(pydantic.BaseModel):   # валидация рекламы

    user_id: Optional[int] = None
    header: Optional[str] = None
    description: Optional[str] = None

    @pydantic.field_validator('user_id')
    async def validate_ad_owner(cls, value):
        response = requests.get(URL + value)
        if response.status_code != 200:
            raise ValueError('user not found...')
        return value

