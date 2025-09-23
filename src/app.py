from ai import AI
from config import load
from disk_cache import DiskCache
from mapgenerator import MapGenerator

from templates import Templates


class App:
    def __init__(self, cache_path: str, config_path: str) -> None:
        self.config = load(config_path)
        self.cache = DiskCache(cache_path)
        self.templates = Templates(self.config)
        self.ai = AI(self.cache, self.templates, self.config)
        self.map_generator = MapGenerator(ai=self.ai, config=self.config)

    def generate_map(self):
        self.map_generator.generate()
