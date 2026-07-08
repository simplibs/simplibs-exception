"""
test_function_is_callable - kontrola předané funkce zda je volatelná (testuje se vždy)
test_valid_input_does_not_raise - test pokud jsou předané valid_value - tak že s nimi vse výjimka nevyvolá (testuje se jen když jsou předané)
test_invalid_input_raises - test pokud jsou předané invalid_value - tak že s nimi vse výjimka vyvolá (testuje se jen když jsou předané)
test_function_raises - test pokud nejsou předané valid_value a invalid_value a tedy spustí se funkce bez parametrů (testuje se jen když nejsou předané)
test_exception_type

test_error_name
test_label
test_message
test_expected
test_value
test_problem
test_context
test_how_to_fix
test_exception
test_get_location
test_skip_locations
test_oneline



✓ valid input

✓ invalid input

✓ exception type

✓ label

✓ expected

✓ problem

✓ context



test_valid_input PASSED
test_invalid_input PASSED
test_label PASSED
...
"""
from typing import Any, Callable
from simplibs.sentinels import UNSET, UnsetType

def assert_simple_exception2(

    # --- Funkce k otestování ---
    func: Callable[..., Any],
    *,
    # --- Natsavení volání ---
    valid_value: Any = UNSET,
    invalid_value: Any = UNSET,
    valid_args: tuple[Any, ...] = (),
    valid_kwargs: dict[str, Any] | None = None,
    invalid_args: tuple[Any, ...] = (),
    invalid_kwargs: dict[str, Any] | None = None,
    exception_type: type[BaseException] = Exception,

    # --- Definice polí ---
    error_name: str | UnsetType = UNSET,
    label: str | None | UnsetType = UNSET,
    message: str | None | UnsetType = UNSET,
    expected: str | None | UnsetType = UNSET,
    value: Any = UNSET,
    problem: "str | tuple[str, ...] | None | UnsetType" = UNSET,
    context: "str | tuple[str, ...] | None | UnsetType" = UNSET,
    how_to_fix: "str | tuple[str, ...] | None | UnsetType" = UNSET,
    exception: "Exception | type[Exception] | None | UnsetType" = UNSET,
    get_location: "bool | int | UnsetType" = UNSET,
    skip_locations: "tuple[str, ...] | UnsetType" = UNSET,
    oneline: "bool | UnsetType" = UNSET,

) -> BaseException | None:...

