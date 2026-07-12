from dataclasses import dataclass
from typing import Any, Callable
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ..assert_exception_function import assert_exception_function


@dataclass(slots=True, kw_only=True)
class FunctionCase:
    """A declarative, reusable container representing an isolated functional test scenario.

    Captures and stores the entire static expectation blueprint required to validate
    an exception-producing function boundary. It intentionally decouples runtime execution
    settings to allow scenarios to be dynamically orchestrated by matrix runners.

    Attributes:
        func: The target callable validation or logic function under test.
        valid_param: An optional parameter payload expected to pass without error.
        invalid_param: The parameter payload expected to trigger the exception.
        exception_type: The expected exception class type blueprint.
        error_name: Expected internal system error identity code.
        label: Expected human-readable categorization title.
        message: Expected dynamic text body or terminal explanation block.
        expected: Expected value or state description criteria.
        value: Expected raw problematic value or object state.
        problem: Expected breakdown sequence or root cause description.
        context: Expected technical parameters or surrounding metrics.
        how_to_fix: Expected structured actionable recommendations.
        exception: Expected raw intercept nested exception instance.
        get_location: Expected active relative stack scanning frame trace.
        skip_locations: Expected global or contextual exclusion string path filter.
        oneline: Expected strict structural flag enforcing flat single-line message.
    """

    func: Callable[..., Any]
    exception_type: type[BaseException]

    valid_param: Any = UNSET
    invalid_param: Any = UNSET

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
        exact_match: bool = False,
        startswith: bool = False,
        verbose: bool = True,
        intro: str = "",
        deep_check: bool = True,
    ) -> BaseException:
        """Execute this test scenario directly against the underlying functional intercept engine.

        Proxies stored attributes down to `assert_exception_function`. Default comparison
        mode is fuzzy substring inclusion.

        Args:
            subtests: The native pytest subtests fixture manager instance.
            exact_match: If True, enforces strict exact equality.
            startswith: If True, validates that the actual value starts with the expected value.
            verbose: If True, registers individual telemetry property checks as subtests.
            intro: Custom namespace prefix string attached to subtest names.
            deep_check: Flags whether the targeted evaluations apply rigorous compliance maps.

        Returns:
            The caught, instantiated live exception object.
        """
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
            startswith=startswith,
            verbose=verbose,
            intro=intro,
            deep_check=deep_check,
        )


_DESIGN_NOTES = """
# FunctionCase (Declarative Functional Test Scenario Blueprint)

## Architectural Purpose
`FunctionCase` acts as a specialized data schema wrapper for functional boundary testing, 
pairing an anonymous executable routine (`func`) with a comprehensive block of concrete 
diagnostic expectations.

## Comparison Modalities (Opt-in Architecture)
The test engine defaults to substring inclusion (`in` operator), providing the most resilient 
audit for dynamic error messages. Stricter validation modes require explicit opt-in:
- **`exact_match=True`**: Full string equality.
- **`startswith=True`**: Prefix validation.

## Tactical Domain Selection
- **Exception Classes:** Do **not** use `FunctionCase`. 
- **Functions & Logic Gates:** Natively wrapped via `FunctionCase` whenever deep telemetry 
  property validation is required.

## Matrix Orchestration Compatibility
`FunctionCase` serves as a premium object format within `generate_bulk_tests`. This allows 
developers to construct visual and readable test batteries where structural class audits 
and intricate multi-point logic verifications sit side-by-side inside a single master 
collection layout.
"""