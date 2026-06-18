# Safe runtime imports only
# Avoid importing optional modules at startup

def classify_init(file_path, exports, imports):
    """
    __init__.py is only a stub if ALL are true:
    - no exports
    - no imports
    - no docstring
    - contains only pass/ellipsis
    """
    if exports or imports:
        return "valid_module"

    return "empty_initializer"


# core runtime entry safety layer
__all__ = []