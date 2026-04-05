from __future__ import annotations

from dataclasses import dataclass

from app.users import User
from app.switchboard_utils import create_user_based_on_phone_number


LOCAL_PHONE_PREFIX = "+7"
RAW_CALL_SEPARATOR = ","


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

        users_info = raw_call.split(RAW_CALL_SEPARATOR)
        if len(users_info) != 6:
            raise ValueError("'raw_call' should look like this "
                             "'caller_id,caller_name,caller_phone,receiver_id,receiver_name,receiver_phone'")

        if '' in users_info or ' ' in users_info:
            raise ValueError("'raw_call' values should not be empty or contain white spaces")

        if '-' in users_info[0] or '-' in users_info[3]:
            raise ValueError("'caller_id' or 'receiver_id' should represent positive int")

        if users_info[0].isdigit() is False or users_info[3].isdigit() is False:
            raise ValueError("'caller_id' or 'receiver_id' should be parsable to int")

        caller = create_user_based_on_phone_number(int(users_info[0]), users_info[1], users_info[2])
        receiver = create_user_based_on_phone_number(int(users_info[3]), users_info[4], users_info[5])

        active_call = ActiveCall(caller=caller, receiver=receiver)
        if active_call.is_cross_border:
            self._cross_border_calls_count += 1
        self._active_calls.append(active_call)

        return active_call

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self._cross_border_calls_count
