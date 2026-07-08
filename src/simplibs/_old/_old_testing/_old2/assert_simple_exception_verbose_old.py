import pytest
from typing import Any, Callable, TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
from ..SimpleException import SimpleException
from ..protocols import SimpleExceptionProtocol




def manage_param(param):
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}
    if isinstance(param, dict):
        if param:  # neprázdný dict → kwargs
            kwargs = param
        else:  # prázdný dict → positional
            args = (param,)
    elif isinstance(param, (tuple, list)):
        if param:  # neprázdný tuple/list → args
            args = tuple(param)
        else:  # prázdný tuple/list → positional
            args = (param,)
    else:
        # cokoliv jiného (včetně "", set(), b"", None, 0, False)
        args = (param,)

    return args, kwargs

def compare_strings(test_value, exc_value, exact_match):
    if exact_match:
        assert test_value == exc_value
    else:
        if isinstance(test_value, tuple):
            test_value = " ".join(test_value)
        if isinstance(exc_value, tuple):
            exc_value = " ".join(exc_value)
        assert test_value in exc_value

def assert_simple_exception_verbose(
    # --- Subtest ----
    subtests,

    # --- Funkce k otestování ---
    func: Callable[..., Any],
    *,
    # --- Natsavení volání ---
    valid_param: Any = UNSET,
    invalid_param: Any = UNSET,
    exception_type: type[SimpleException] = SimpleException,

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

    # --- Doplňující parametr pro způsob validace ---
    exact_match: bool = True,

) -> BaseException | None:


    # 1. Kontrola zda je funkce callable
    with subtests.test("test_function_is_callable"):
        assert callable(func)

    # 2. Kontrola zda projdou validní argunmenty
    if valid_param is not UNSET:
        args, kwargs = manage_param(valid_param)
        with subtests.test("test_valid_input"):
            func(*args, **kwargs)


    # 3. Kontrola vyvolání výjimky
    # 3.1 Definice prázdných parametrů
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}

    # 3.2 naplnění parametrů - jsou li přdány
    if invalid_param is not UNSET:
        args, kwargs = manage_param(invalid_param)

    # 3.3 Vyvolání výjimky a ověření typu výjimky + načtení dat výjimky
    with subtests.test("test_function_raise_exception"):
        with pytest.raises(exception_type) as exc_info:
            func(*args, **kwargs)

    # 4. Načtení dat výjimky
    exc = exc_info.value

    # 5. Kontrola error_name
    if error_name is not UNSET:
        with subtests.test("test_error_name"):
            compare_strings(error_name, exc.error_name, exact_match)

    # 6. Kontrola label
    if label is not UNSET:
        with subtests.test("test_label"):
            compare_strings(label, exc.label, exact_match)

    # 7. Kontrola message
    if message is not UNSET:
        with subtests.test("test_message"):
            compare_strings(message, exc.message, exact_match)

    # 8. Kontrola expected
    if expected is not UNSET:
        with subtests.test("test_expected"):
            compare_strings(expected, exc.expected, exact_match)

    # 9. Kontrola value
    if value is not UNSET:
        with subtests.test("test_value"):
            assert value == exc.value

    # 10. Kontrola problem
    if problem is not UNSET:
        with subtests.test("test_problem"):
            compare_strings(problem, exc.problem, exact_match)

    # 11. Kontrola context
    if context is not UNSET:
        with subtests.test("test_context"):
            compare_strings(context, exc.context, exact_match)

    # 12. Kontrola how_to_fix
    if how_to_fix is not UNSET:
        with subtests.test("test_how_to_fix"):
            compare_strings(how_to_fix, exc.how_to_fix, exact_match)

    # 13. Kontrola exception
    if exception is not UNSET:
        with subtests.test("test_exception"):
            assert exception == exc.exception

    # 14. Kontrola get_location
    if get_location is not UNSET:
        with subtests.test("test_get_location"):
            assert get_location == exc.get_location

    # 15. Kontrola get_location
    if skip_locations is not UNSET:
        with subtests.test("test_skip_locations"):
            assert skip_locations == exc.skip_locations

    # 16. Kontrola oneline
    if oneline is not UNSET:
        with subtests.test("test_oneline"):
            assert oneline == exc.oneline