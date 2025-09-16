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

    def generate_map(self, seed: int):
        map = self.ai.generate_map(seed)
        with self.gui_controller as gui_controller:
            logger.debug(f"Display: {os.environ.get('DISPLAY')}")
            gui_controller.prepare()
            logger.debug("Generating the map")
            self.map_generator.generate(map, gui_controller)
