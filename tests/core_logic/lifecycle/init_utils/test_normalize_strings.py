from simplibs.exception._core_logic.lifecycle.init_utils.normalize_strings import (
    normalize_strings,
)


class Dummy:
    problem = "default-problem"


def test_string_input_returned_as_is():
    instance = Dummy()
    assert normalize_strings(instance, "single line problem", "problem") == "single line problem"


def test_list_with_single_item_is_flattened_to_str():
    instance = Dummy()
    result = normalize_strings(instance, ["only one"], "problem")
    assert result == "only one"
    assert isinstance(result, str)


def test_tuple_with_multiple_items_stays_a_tuple():
    instance = Dummy()
    result = normalize_strings(instance, ("first", "second"), "problem")
    assert result == ("first", "second")


def test_list_items_are_stripped_and_empty_ones_removed():
    instance = Dummy()
    result = normalize_strings(instance, ["  first  ", "", "   ", "second"], "problem")
    # Only non-empty entries survive; note the function keeps items as-is
    # (not stripped values) except that blank/whitespace-only ones are dropped.
    assert result == ("  first  ", "second")


def test_non_string_items_in_list_are_filtered_out():
    instance = Dummy()
    result = normalize_strings(instance, ["valid", 123, None, "also valid"], "problem")
    assert result == ("valid", "also valid")


def test_list_with_no_valid_strings_falls_back_to_default():
    instance = Dummy()
    result = normalize_strings(instance, [123, None, "   "], "problem")
    assert result == "default-problem"


def test_invalid_type_falls_back_to_default():
    instance = Dummy()
    assert normalize_strings(instance, 42, "problem") == "default-problem"


def test_none_falls_back_to_default():
    instance = Dummy()
    assert normalize_strings(instance, None, "problem") == "default-problem"


def test_falls_back_to_none_when_no_class_default_defined():
    class NoDefault:
        pass

    instance = NoDefault()
    assert normalize_strings(instance, 42, "problem") is None
