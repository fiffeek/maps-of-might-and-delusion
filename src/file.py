import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def os_expand(path: str) -> str:
    return os.path.expandvars(path)


def ensure_dir_exists(path: str):
    os.makedirs(path, exist_ok=True)
