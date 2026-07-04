def print_multiline(
    prefix: str = "",
    texts: tuple[str, ...] | None = None,
    log_mode: bool = False
) -> str | None:
    """
    Renders the exception's context. Supporting single or multi-line
    outputs aligned perfectly under the prefix header, or formatted cleanly for logs.
    """
    if isinstance(texts, str):
        return print_oneline(prefix, texts, log_mode)

    if not texts:
        return None

    # 1. LOG MODE: Flatten all lines into a single string for machine processing
    if log_mode:
        flat_context = " ".join(texts)
        return f"{prefix}{flat_context!r}"

    # 2. STANDARD MODE: Inline first item, align subsequent items via EMPTY_PREFIX
    first_line = texts[0]
    remaining_lines = texts[1:]

    if not remaining_lines:
        return prefix + first_line

    return prefix + first_line + EMPTY_PREFIX + EMPTY_PREFIX.join(remaining_lines)
