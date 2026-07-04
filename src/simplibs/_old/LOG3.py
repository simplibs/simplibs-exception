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
    print_file_info,
    print_file_path
)

class LogMessage(ModeBase):
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
            print_intro(data.error_name, data.label, _log_mode=True),

            # 2. Jádro zprávy a strukturované detaily
            print_message(data.message, _log_mode=True),
            print_expected(data.expected, _log_mode=True),
            print_value_with_type(data.value, _log_mode=True),
            print_problem(data.problem, _log_mode=True),
            print_context(data.context, _log_mode=True),

            # 3. Společná metadata o poloze souboru
            print_file_info(location, _log_mode=True),
            print_file_path(location, _log_mode=True),
        ]

        # Spojíme pouze existující řádky – prázdná místa po chybějících datech zmizí
        return " ".join(line for line in lines if line)