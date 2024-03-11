import re

from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

from .books import ReturnedSellerBooks

__all__ = ["IncomingSeller", "ReturnedAllSellers", "ReturnedSeller", "ReturnerSellerAllBooks"]

def check_email(email):
    pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$' 
    return re.match(pattern, email)


# Базовый класс "Seller", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str


# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    password: str

    @field_validator("email")  # Валидатор, проверяет что дата не слишком древняя
    @staticmethod
    def check_email(val: str):
        if check_email(val):
            return val
        raise PydanticCustomError("Validation error", "Year is wrong!")


# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedSeller(BaseSeller):
    id: int


# Класс для возврата массива объектов "Seller"
class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]


# Класс для возврата массива объектов "Seller" с полями "Book"
class ReturnerSellerAllBooks(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    books: list[ReturnedSellerBooks]
