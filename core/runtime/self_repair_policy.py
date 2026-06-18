IGNORED_PATTERNS = {
    "__init__.py": "always_valid_package_marker",
    "setup.py": "build_entrypoint",
    "version.py": "metadata",
    "__main__.py": "entrypoint",
}


def is_never_delete(file_path: str) -> bool:
    name = file_path.split("/")[-1]
    return name in IGNORED_PATTERNS