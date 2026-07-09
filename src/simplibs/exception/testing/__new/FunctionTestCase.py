from dataclasses import dataclass
from typing import Any, Callable

from simplibs.sentinels import UNSET, UnsetType

from .assert_exception_function import assert_exception_function


@dataclass(slots=True, kw_only=True)
class FunctionTestCase:
    """Represents a reusable exception function test scenario.

    Stores all static expectations required for validating an exception-producing
    function. Runtime execution settings (subtests, verbosity, deep checking, ...)
    are intentionally supplied later by the bulk test runner.
    """

    func: Callable[..., Any]

    valid_param: Any = UNSET
    invalid_param: Any = UNSET

    exception_type: type[BaseException]

    error_name: str | UnsetType = UNSET
    label: str | None | UnsetType = UNSET
    message: str | None | UnsetType = UNSET
    expected: str | None | UnsetType = UNSET
    value: Any = UNSET
    problem: str | tuple[str, ...] | None | UnsetType = UNSET
    context: str | tuple[str, ...] | None | UnsetType = UNSET
    how_to_fix: str | tuple[str, ...] | None | UnsetType = UNSET
    exception: Exception | type[Exception] | None | UnsetType = UNSET
    get_location: bool | int | UnsetType = UNSET
    skip_locations: tuple[str, ...] | UnsetType = UNSET
    oneline: bool | UnsetType = UNSET

    def run_test(
        self,
        subtests: Any,
        *,
        exact_match: bool = True,
        verbose: bool = True,
        intro: str = "",
        deep_check: bool = True,
    ) -> BaseException:
        """Execute this test case."""

        return assert_exception_function(
            subtests,
            self.func,

            valid_param=self.valid_param,
            invalid_param=self.invalid_param,

            exception_type=self.exception_type,

            error_name=self.error_name,
            label=self.label,
            message=self.message,
            expected=self.expected,
            value=self.value,
            problem=self.problem,
            context=self.context,
            how_to_fix=self.how_to_fix,
            exception=self.exception,
            get_location=self.get_location,
            skip_locations=self.skip_locations,
            oneline=self.oneline,

            exact_match=exact_match,
            verbose=verbose,
            intro=intro,
            deep_check=deep_check,
        )