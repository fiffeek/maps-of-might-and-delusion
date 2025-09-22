import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def os_expand(path: str) -> str:
    return os.path.expandvars(path)


def ensure_dir_exists(path: str):
    os.makedirs(path, exist_ok=True)


def write_file(path: str, content: str):
    path = os_expand(path)
    ensure_dir_exists(os.path.dirname(path))
    with open(path, "w+") as f:
        f.write(content)
