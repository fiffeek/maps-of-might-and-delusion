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
        self.ai = AI(self.cache)
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
        self.map_generator = MapGenerator(ai=self.ai)

    def generate_map(self, seed: int, save_directory: str):
        self.map_generator.generate(seed, save_directory)

    def run_standalone_vcmi(self):
        with self.gui_controller as gui_controller:
            logger.debug(f"Display: {os.environ.get('DISPLAY')}")
            gui_controller.prepare()
            gui_controller.new_map(MapSize.S)
            self.vcmi.stream_logs()
