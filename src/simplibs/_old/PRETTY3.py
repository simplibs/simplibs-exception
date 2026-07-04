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

class PrettyMessage(ModeBase):
    """Structured output framed with double lines — the default mode."""

    def full_outcome(
        self: "ModeBaseProtocol",
        data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Dynamically adapts and renders the exception into a beautiful framed output.
        Handles empty, message-only, and fully structured data seamlessly.
        """
        location = data.caller_info

        # 1. Zjistíme, zda máme podrobná strukturovaná data pro tělo výpisu
        has_details = any([
            data.expected,
            data.value is not UNSET,
            data.problem,
            data.context
        ])

        lines = [
            DOUBLE_LINE,
            print_intro(data.error_name, data.label),

            # 2. Druhá linka se vykreslí POUZE, pokud následují strukturované detaily
            DOUBLE_LINE if has_details else None,

            # 3. Jádro zprávy a detaily (minifunkce vrátí None, pokud data chybí)
            print_message(data.message),
            print_expected(data.expected),
            print_value_with_type(data.value, intro="Got:       "),
            print_problem(data.problem),
            print_context(data.context),

            # 4. Společná metadata o poloze souboru
            print_file_info(location),
            print_file_path(location),

            # 5. Blok pro nápravu (How to fix)
            SINGLE_LINE if data.how_to_fix else None,
            print_how_to_fix(data.how_to_fix),

            DOUBLE_LINE,

            # 6. Případná zachycená výjimka na samém dospodu
            print_intercepted_exception(data.exception, data.intercepted_exception)
        ]

        return "\n".join(line for line in lines if line)