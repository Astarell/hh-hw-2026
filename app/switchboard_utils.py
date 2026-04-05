from app.users import User
from app.users import ForeignUser, LocalUser

# Из switchboard.py константу можно удалить, при импорте возникали ошибки
LOCAL_PHONE_PREFIX = "+7"

def is_local_user(phone_number: str) -> bool:
    return phone_number.startswith(LOCAL_PHONE_PREFIX)

def create_user_based_on_phone_number(user_id: int, user_name: str, user_phone_number: str) -> User:
    if is_local_user(user_phone_number):
        return LocalUser(user_id, user_name, user_phone_number)
    return ForeignUser(user_id, user_name, user_phone_number)