from dataclasses import dataclass
from typing import Any, Callable
from simplibs.sentinels import UNSET, UnsetType
 # Outers
from ..asserts import assert_exception_function


@dataclass(slots=True, kw_only=True)
class TestCase:
    """A declarative, reusable container representing an isolated functional test scenario.

    Captures and stores the entire static expectation blueprint required to validate
    an exception-producing function boundary. It intentionally decouples runtime execution
    settings (such as the pytest subtests manager, verbosity, or matching modes) to allow
    the scenario to be dynamically orchestrated by higher-level matrix runners.

    Attributes:
        func: The target callable validation or business logic function under test.
        valid_param: An optional parameter payload (scalar, tuple, list, or Kwargs) expected
            to pass execution successfully without raising any exception.
        invalid_param: The parameter payload (scalar, tuple, list, or Kwargs) expected to
            breach operational rules and trigger the target exception type.
        exception_type: The expected exception class type blueprint that should be intercepted.
        error_name: Expected internal system error identity code or unique string slug.
        label: Expected human-readable categorization title or layer indicator.
        message: Expected dynamic text body or terminal explanation block.
        expected: Expected value or state description criteria that was breached.
        value: Expected raw problematic value or object state that triggered the exception.
        problem: Expected description or breakdown of the concrete malfunction root causes.
        context: Expected technical parameters or surrounding environmental metrics.
        how_to_fix: Expected structured actionable recommendations or remediation paths.
        exception: Expected raw intercept nested exception instance or underlying class type.
        get_location: Expected active relative stack scanning frame trace setting indicator.
        skip_locations: Expected global or contextual exclusion string path filter collection.
        oneline: Expected strict structural flag enforcing flat single-line message layouts.
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
        """Execute this test scenario directly against the underlying functional intercept engine.

        Proxies the stored attributes down to `assert_exception_function` alongside
        the supplied live context parameters.

        Args:
            subtests: The native pytest subtests fixture manager instance.
            exact_match: When True, enforces strict exact equality. When False, switches
                string checks to fuzzy substring inclusion lookups. Defaults to True.
            verbose: If True, registers individual telemetry property checks under independent
                pytest subtest keys. Defaults to True.
            intro: Custom namespace prefix string attached to subtest names for better grouping.
            deep_check: Flags whether the targeted evaluations apply rigorous compliance maps.

        Returns:
            The caught, instantiated live exception object for further custom client assertions.
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
            verbose=verbose,
            intro=intro,
            deep_check=deep_check,
        )


_DESIGN_NOTES = """
# TestCase (Declarative Functional Test Scenario Blueprint)

## Architectural Purpose
`TestCase` acts as a specialized data schema wrapper designed specifically for functional boundary testing. 
While raw exception classes (`SimpleExceptionData` subclasses) natively encode their own default 
telemetry properties within their class bodies, an executable *function* possesses no such metadata. 

Therefore, `TestCase` fills this structural gap by pairing an anonymous executable routine (`func`) 
with a comprehensive block of concrete diagnostic expectations.

## Tactical Domain Selection
- **Exception Classes:** Do **not** use `TestCase`. Exception classes are self-contained and are 
  passed raw directly to the matrix runner, which extracts data using reflection mapping.
- **Functions & Logic Gates:** Natively wrapped via `TestCase` whenever deep telemetry property validation 
  (messages, labels, remediation steps) is required during mass automated matrix runs.

## Matrix Orchestration Compatibility
While `TestCase` exposes a direct `.run_test()` short-circuit execution capability, its primary ecosystem 
role is serving as a premium object format within `generate_bulk_tests`. This allows developers to construct 
highly visual and readable test batteries where structural class audits and intricate multi-point logic 
verifications sit side-by-side inside a single master collection layout.
"""