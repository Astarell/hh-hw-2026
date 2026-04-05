import pytest

from app.switchboard import Switchboard
from app.switchboard_utils import is_local_user, create_user_based_on_phone_number
from app.users import ForeignUser, LocalUser


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1


def test_register_call_when_input_empty_then_should_raise_value_error_exception() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="'raw_call' should not be empty"):
        switchboard.register_call("")


def test_register_call_when_input_cannot_be_separated_by_expected_delimiter_then_should_raise_value_error_exception() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="'raw_call' should have expected separators"):
        switchboard.register_call("1")


def test_register_call_when_input_str_list_contains_incorrect_number_of_values_then_should_raise_value_error_exception() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="'raw_call' should look like this "
                             "'caller_id,caller_name,caller_phone,receiver_id,receiver_name,receiver_phone'"):
        switchboard.register_call("1,2,3,4,5")


@pytest.mark.parametrize("input", [
    "1,name_1,+79122222222,4,name_2, ",
    "1,name_1,+79122222222,4,name_2,",
])
def test_register_call_when_input_str_list_contains_empty_or_white_space_values_then_should_raise_value_error_exception(input) -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="'raw_call' values should not be empty or contain white spaces"):
        switchboard.register_call(input)


@pytest.mark.parametrize("input", [
    "-1,name_1,+79122222222,4,name_2, +79123333333",
    "1,name_1,+79122222222,-4,name_2, +79123333333",
])
def test_register_call_when_caller_id_and_receiver_id_negatives_then_should_raise_value_error_exception(input) -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="'caller_id' or 'receiver_id' should represent positive int"):
        switchboard.register_call(input)


@pytest.mark.parametrize("input", [
    "1_n,name_1,+79122222222,4,name_2, +79123333333",
    "1,name_1,+79122222222,4_n,name_2, +79123333333",
])
def test_register_call_when_caller_id_and_receiver_id_cannot_be_parsed_to_int_then_should_raise_value_error_exception(input) -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="'caller_id' or 'receiver_id' should be parsable to int"):
        switchboard.register_call(input)


# Проверки switchboard_utils.py лучше бы вынести в отдельный файл, но по заданию все изменения по тестам должны быть тут
# (Не считая класс-утиль :) )
def test_is_local_user_when_starts_with_plus7_then_should_return_true() -> None:
    assert is_local_user("+79122222222") == True


def test_is_local_user_when_not_starts_with_plus7_then_should_return_true() -> None:
    assert is_local_user("+129122222222") == False


def test_create_user_based_on_phone_number_when_local_phone_then_should_return_local_user_instance() -> None:
    local_user = create_user_based_on_phone_number(1, "name_1", "+79122222222")
    assert isinstance(local_user, LocalUser)
    assert local_user.user_type() == "local"


def test_create_user_based_on_phone_number_when_foreign_phone_then_should_return_foreign_user_instance() -> None:
    local_user = create_user_based_on_phone_number(1, "name_1", "+12122222222")
    assert isinstance(local_user, ForeignUser)
    assert local_user.user_type() == "foreign"