"""
A tiny helper module living in its own file, used only so tests can verify
that `excluded_patterns` correctly skips frames based on *file path*
(this module's filename), not function name.
"""

from simplibs.exception._core_logic.tracing.extract_caller_info import (
    extract_caller_info,
)


def call_extract_caller_info(expected_frames=1, excluded_patterns=()):
    return extract_caller_info(
        expected_frames=expected_frames, excluded_patterns=excluded_patterns
    )
