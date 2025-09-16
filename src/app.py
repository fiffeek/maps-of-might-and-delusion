import time
import os

from ai import AI
from disk_cache import DiskCache
from gui import GUIController, VCMI
from mapgenerator import MapGenerator
from logger import logger
import docker


class Application:
    def __init__(
        self,
        cache_path: str,
        homm_data_path: str,
        repository: str,
        tag: str,
        display: int,
        xauth_dir: str,
    ) -> None:
        self.cache = DiskCache(cache_path)
        self.ai = AI(cache=self.cache)
        self.docker_client = docker.from_env()
        self.virtual_display = VCMI(
            repository=repository,
            tag=tag,
            homm_data_path=homm_data_path,
            docker_client=self.docker_client,
            display=display,
            xauth_mount_dir=xauth_dir,
        )
        self.gui_controller = GUIController(self.virtual_display)
        self.map_generator = MapGenerator()

    def generate_map(self):
        map = self.ai.generate_map()
        with self.gui_controller:
            logger.debug("Generating the map")
            logger.debug(f"Display: {os.environ.get('DISPLAY')}")
            time.sleep(20)
            self.map_generator.generate(map, self.gui_controller)
