"""

3. assert_exception_class_structure()

Tady bych naopak vůbec neřešil hodnoty.

Pouze architekturu.

Například:

assert issubclass(exc_class, SimpleExceptionData)

exc = exc_class()

assert isinstance(str(exc), str)

if hasattr(exc, "to_dict"):
    ...

if hasattr(exc, "to_debug_dict"):
    ...

Všimni si jedné věci.

Tahle funkce vůbec nepotřebuje znát

message
label
problem
...

Ty s architekturou nijak nesouvisí.
"""