import os

from ai import AI
from disk_cache import DiskCache
from gui import GUIController, VCMI
from mapgenerator import MapGenerator
from logger import logger
import docker

from models import MapSize


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
        try:
            self.ai = AI(cache=self.cache)
        except Exception as e:
            logger.error(f"error while initializing the agent: {e}")
            self.ai = None
        self.docker_client = docker.from_env()
        self.vcmi = VCMI(
            repository=repository,
            tag=tag,
            homm_data_path=homm_data_path,
            docker_client=self.docker_client,
            display=display,
            xauth_mount_dir=xauth_dir,
        )
        self.gui_controller = GUIController(self.vcmi)
        self.map_generator = MapGenerator()

    def generate_map(self, seed: int):
        if self.ai is None:
            raise RuntimeError("ai agent is None")
        map = self.ai.generate_map(seed)
        # with self.gui_controller as gui_controller:
        # logger.debug(f"Display: {os.environ.get('DISPLAY')}")
        # gui_controller.prepare()
        # logger.debug("Generating the map")
        self.map_generator.generate(map)

    def run_standalone_vcmi(self):
        with self.gui_controller as gui_controller:
            logger.debug(f"Display: {os.environ.get('DISPLAY')}")
            gui_controller.prepare()
            gui_controller.new_map(MapSize.S)
            self.vcmi.stream_logs()
