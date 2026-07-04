def print_oneline(
    prefix: str = "",
    text: str | None = None,
    log_mode: bool = False
) -> str | None:

    if not text:
        return None

    _text = f"{text!r}" if log_mode else text

    return f"{prefix}{_text}"
