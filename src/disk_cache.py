import os
import hashlib
from typing import Optional
from file import ensure_dir_exists, os_expand


class DiskCache:
    def __init__(self, cache_path: str) -> None:
        self.cache_path = os_expand(cache_path)
        ensure_dir_exists(self.cache_path)

    def upsert(self, key: str, value: str) -> None:
        hash_key = self.hash(key)
        file_path = os.path.join(self.cache_path, f"{hash_key}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(value)

    def get(self, key: str) -> Optional[str]:
        hash_key = self.hash(key)
        file_path = os.path.join(self.cache_path, f"{hash_key}.txt")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def hash(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode("utf-8")).hexdigest()
