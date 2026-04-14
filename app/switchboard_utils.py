import re

from app.users import User
from app.users import ForeignUser, LocalUser

# Из switchboard.py константу можно удалить, при импорте возникали ошибки
LOCAL_PHONE_PREFIX = "+7"
PHONE_NUMBER_REGEX = r"^(?=(?:\D*\d){7,15}\D*$)(?:\+|8)?[\d\s()-]{7,20}$"

def is_local_user(phone_number: str) -> bool:
    return phone_number.startswith(LOCAL_PHONE_PREFIX)

def create_user_based_on_phone_number(user_id: int, user_name: str, user_phone_number: str) -> User:
    if is_local_user(user_phone_number):
        return LocalUser(user_id, user_name, user_phone_number)
    return ForeignUser(user_id, user_name, user_phone_number)

# Написать необходимый паттерн для проверки номера телефона
def is_phone_valid(phone_number: str) -> bool:
    return re.fullmatch(PHONE_NUMBER_REGEX, phone_number) is not None