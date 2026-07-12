# Normalize inputs to strings (handles None, Unset, and tuples)
    def normalize(val) -> str:
        if val is None or isinstance(val, UnsetType):
            return ""
        if isinstance(val, tuple):
            return " ".join(val)
        return val