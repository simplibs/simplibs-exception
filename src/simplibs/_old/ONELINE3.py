from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .base_class import ModeBase
from .printers.constants import DOUBLE_LINE, SINGLE_LINE, DOT_PREFIX
# from .printers.methods import print_caller_info, print_intro_line, print_value_with_type
# Annotations
if TYPE_CHECKING:
    from ..protocols import ModeBaseProtocol
    from ..protocols import SimpleExceptionDataProtocol

from .printers.methods.full_outcome import (
    print_message,
    print_intro,
    print_expected,
    print_value_with_type,
    print_problem,
    print_context,
    print_how_to_fix,
    print_intercepted_exception,
    print_file_info,
    print_file_path
)


class OnelineMessage(ModeBase):
    """Compact single-line output for terminal use and quick debugging."""

    def full_outcome(
        self: "ModeBaseProtocol",
        data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Dynamically adapts and flattens all available exception fields into
        a single, pipe-separated string. Handles all data states automatically.
        """

        # Skládáme jednotlivé části do jednoho plochého seznamu
        parts = [
            # 1. Hlavní úvod (⚠️ ERROR NAME: label)
            print_intro(data.error_name, data.label),

            # 2. Strukturovaná data (minifunkce vrátí None, pokud data chybí)
            print_message(data.message),
            print_expected(data.expected),
            print_value_with_type(data.value, intro="Got: "),
            print_problem(data.problem),
            print_context(data.context),
            print_file_info(data.caller_info),
            print_file_path(data.caller_info),
        ]

        # Spojíme všechny platné kousky pomocí " | " a ořežeme případné zbytečné mezery
        return " | ".join(part for part in parts if part).strip()