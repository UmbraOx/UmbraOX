CORE_PROTECTED = {
    "__init__.py",
    "__main__.py",
    "setup.py",
    "runtime_self_repair_core.py"
}


def is_protected(file_name: str) -> bool:
    return file_name in CORE_PROTECTED