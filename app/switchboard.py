from __future__ import annotations

from dataclasses import dataclass

from app.users import User
from app.switchboard_utils import create_user_based_on_phone_number, is_phone_valid

LOCAL_PHONE_PREFIX = "+7"
RAW_CALL_SEPARATOR = ","

FIRST_USER_ID_IDX = 0
FIRST_USER_NAME_IDX = 1
FIRST_USER_PHONE_IDX = 2

SECOND_USER_ID_IDX = 3
SECOND_USER_NAME_IDX = 4
SECOND_USER_PHONE_IDX = 5


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._cross_border_calls_count: int = 0 # Для константного времени при get_cross_border_calls_count(self)

    # Сначала думал вынести проверки в класс утиль, но далее передумал, тк здесь намного нагляднее получается
    # Сразу по коду понятно из-за чего и почему может быть исключение в этом методе
    # Но для чистоты можно рассмотреть первоначальный вариант
    def register_call(self, raw_call: str) -> ActiveCall:

        if len(raw_call) == 0:
            raise ValueError("'raw_call' should not be empty")

        if RAW_CALL_SEPARATOR not in raw_call:
            raise ValueError("'raw_call' should have expected separators")

        users_info = [x.strip() for x in raw_call.split(RAW_CALL_SEPARATOR)]
        if len(users_info) != 6:
            raise ValueError("'raw_call' should look like this "
                             "'caller_id,caller_name,caller_phone,receiver_id,receiver_name,receiver_phone'")

        if '' in users_info or ' ' in users_info:
            raise ValueError("'raw_call' values should not be empty or contain white spaces")

        if users_info[FIRST_USER_ID_IDX].isdigit() is False or users_info[SECOND_USER_ID_IDX].isdigit() is False:
            raise ValueError("'caller_id' or 'receiver_id' should be parsable to int and positive int")

        if is_phone_valid(users_info[FIRST_USER_PHONE_IDX]) is False or is_phone_valid(
                users_info[SECOND_USER_PHONE_IDX]) is False:
            raise ValueError("Phone number should be valid")

        caller = create_user_based_on_phone_number(int(users_info[FIRST_USER_ID_IDX]),
                                                   users_info[FIRST_USER_NAME_IDX],
                                                   users_info[FIRST_USER_PHONE_IDX])
        receiver = create_user_based_on_phone_number(int(users_info[SECOND_USER_ID_IDX]),
                                                     users_info[SECOND_USER_NAME_IDX],
                                                     users_info[SECOND_USER_PHONE_IDX])

        active_call = ActiveCall(caller=caller, receiver=receiver)
        if active_call.is_cross_border:
            self._cross_border_calls_count += 1
        self._active_calls.append(active_call)

        return active_call

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self._cross_border_calls_count
