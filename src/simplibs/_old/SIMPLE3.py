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

class SimpleMessage(ModeBase):
    """Output without decorative lines — plain text layout."""

    def full_outcome(
        self: "ModeBaseProtocol",
        data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Dynamically adapts and renders the exception into a clean plain text layout.
        Handles empty, message-only, and fully structured data seamlessly.
        """
        location = data.caller_info

        lines = [
            # 1. Hlavní úvodní řádek (⚠️ ERROR NAME: label)
            print_intro(data.error_name, data.label),

            # 2. Jádro zprávy a strukturované detaily
            print_message(data.message),
            print_expected(data.expected),
            print_value_with_type(data.value, intro="Got:       "),
            print_problem(data.problem),
            print_context(data.context),

            # 3. Společná metadata o poloze souboru
            print_file_info(location),
            print_file_path(location),

            # 4. Blok pro nápravu (How to fix)
            print_how_to_fix(data.how_to_fix),

            # 5. Případná zachycená výjimka na samém dospodu
            print_intercepted_exception(data.exception, data.intercepted_exception)
        ]

        # Spojíme pouze existující řádky – prázdná místa po chybějících datech zmizí
        return "\n".join(line for line in lines if line)