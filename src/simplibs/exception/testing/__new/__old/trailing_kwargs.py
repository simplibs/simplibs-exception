def trailing_kwargs(raw_params):
    if raw_params and isinstance(raw_params[-1], dict):
        *args, kwargs = raw_params
    else:
        args = raw_params
        kwargs = {}

    return args, kwargs