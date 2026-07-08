from simplibs.exception._core_logic.lifecycle.init_utils.normalize_strings import (
    normalize_strings,
)


class Dummy:
    """Mock container providing a declarative class-level fallback structure for list/tuple processing."""
    problem = "default-problem"


def test_string_input_returned_as_is():
    """Ensures that a plain single-line string passes through instantly without object wrapper overhead."""
    instance = Dummy()
    assert normalize_strings(instance, "single line problem", "problem") == "single line problem"


def test_list_with_single_item_is_flattened_to_str():
    """
    Validates Smart Unboxing Optimization: supplying a single-element collection must
    automatically unbox the payload into a primitive string container.
    """
    instance = Dummy()
    result = normalize_strings(instance, ["only one"], "problem")
    assert result == "only one"
    assert isinstance(result, str)


def test_tuple_with_multiple_items_stays_a_tuple():
    """Guarantees that a multi-element sequence successfully locks inside an immutable tuple matrix."""
    instance = Dummy()
    result = normalize_strings(instance, ("first", "second"), "problem")
    assert result == ("first", "second")


def test_list_items_are_stripped_and_empty_ones_removed():
    """
    Ensures structural sanitization: empty items or whitespace-only sequence entries
    are automatically discarded by the engine, preserving only valuable text blocks.
    """
    instance = Dummy()
    result = normalize_strings(instance, ["  first  ", "", "   ", "second"], "problem")
    assert result == ("  first  ", "second")


def test_non_string_items_in_list_are_filtered_out():
    """Verifies robustness by filtering out foreign data types (ints, dicts, Nones) from incoming arrays."""
    instance = Dummy()
    result = normalize_strings(instance, ["valid", 123, None, "also valid"], "problem")
    assert result == ("valid", "also valid")


def test_list_with_no_valid_strings_falls_back_to_default():
    """Confirms that if a collection yields zero valid string elements, it falls back to the class schema definition."""
    instance = Dummy()
    result = normalize_strings(instance, [123, None, "   "], "problem")
    assert result == "default-problem"


def test_invalid_type_falls_back_to_default():
    """Validates that passing a completely invalid primitive type triggers a clean fallback sequence."""
    instance = Dummy()
    assert normalize_strings(instance, 42, "problem") == "default-problem"


def test_none_falls_back_to_default():
    """Ensures that explicit None arguments are treated as unconfigured states, reverting to defaults."""
    instance = Dummy()
    assert normalize_strings(instance, None, "problem") == "default-problem"


def test_falls_back_to_none_when_no_class_default_defined():
    """
    Verifies defensive emergency mitigation: if data sanitization fails and the class
    completely lacks a property fallback blueprint, the engine safely returns None.
    """
    class NoDefault:
        pass

    instance = NoDefault()
    assert normalize_strings(instance, 42, "problem") is None


def test_collection_with_one_valid_and_multiple_blank_strings_is_flattened_to_str():
    """
    Architectural Edge Case: Verifies that if a multi-item collection yields exactly one
    valid text element after filtering out whitespace/blank tracks, the unboxing engine
    successfully triggers and flattens the final output into a primitive str.
    """
    instance = Dummy()

    # Input has length of 3, but only 1 item is contextually valid
    result = normalize_strings(instance, ["", "  surviving-line  ", "    "], "problem")

    assert result == "  surviving-line  "
    assert isinstance(result, str)