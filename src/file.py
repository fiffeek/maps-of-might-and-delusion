import os


def os_expand(path: str) -> str:
    return os.path.expandvars(path)


def ensure_dir_exists(path: str):
    os.makedirs(path, exist_ok=True)
