class LogMessage(ModeBase):
    """Structured key=value output for log parsers."""

    def full_outcome(
        self: "ModeBaseProtocol",
        data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Dynamically builds a flat, single-line log-friendly key=value string.
        Automatically escapes strings to prevent log injection.
        """
        loc = data.caller_info

        # 1. Nasbíráme surová data do slovníku (žádný formát pro lidi)
        raw_parts = {
            "error": data.error_name,
            "label": data.label,
            "message": data.message,
            "expected": data.expected,
            "problem": data.problem,
            "context": data.context,
        }

        # 2. Přidáme hodnotu (pokud je nastavená)
        if data.value is not UNSET:
            # Zde můžeme jako jedinou výjimku použít tvůj printer pro získání typu
            raw_parts["value"] = print_value_with_type(data.value, intro="")

        # 3. Přidáme polohu (pokud existuje a není dynamická)
        if loc and not loc["file"].startswith("<"):
            raw_parts["file"] = loc["file"]
            raw_parts["line"] = loc["line"]
            raw_parts["function"] = loc["function"]
            raw_parts["path"] = loc["path"]  # o absolutní cestě mluvím níže

        # 4. Formátování do "key=value" řetězce na jeden řádek
        log_items = []
        for key, val in raw_parts.items():
            if val is not None:
                # !r zajistí, že string bude v uvozovkách a oescapovaný (např. 'Něco\nselhalo')
                # Čísla (jako line) zůstanou jako čísla
                log_items.append(f"{key}={val!r}" if isinstance(val, str) else f"{key}={val}")

        # Logy MUSÍ být vždy spojené mezerou a na jednom řádku!
        return " ".join(log_items)