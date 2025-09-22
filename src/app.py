import os

from ai import AI
from config import load
from disk_cache import DiskCache
from gui import GUIController, VCMI
from mapgenerator import MapGenerator
from logger import logger
import docker

from models import MapSize
from templates import Templates


class GeneratorApp:
    def __init__(self, cache_path: str, config_path: str) -> None:
        self.config = load(config_path)
        self.cache = DiskCache(cache_path)
        self.templates = Templates(self.config)
        self.ai = AI(self.cache, self.templates, self.config)
        self.map_generator = MapGenerator(ai=self.ai, config=self.config)

    def generate_map(self):
        self.map_generator.generate()


class VCMIGeneratorApp:
    def __init__(
        self,
        cache_path: str,
        homm_data_path: str,
        repository: str,
        tag: str,
        display: int,
        xauth_dir: str,
        config_path: str,
    ) -> None:
        self.config = load(config_path)
        self.templates = Templates(self.config)
        self.cache = DiskCache(cache_path)
        self.ai = AI(self.cache, self.templates, self.config)
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
        self.map_generator = MapGenerator(ai=self.ai, config=self.config)

    def generate_map(self):
        self.map_generator.generate()


class StandaloneVCMI:
    def __init__(
        self,
        homm_data_path: str,
        repository: str,
        tag: str,
        display: int,
        xauth_dir: str,
    ) -> None:
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

    def run_standalone_vcmi(self):
        with self.gui_controller as gui_controller:
            logger.debug(f"Display: {os.environ.get('DISPLAY')}")
            gui_controller.prepare()
            gui_controller.new_map(MapSize.SMALL)
            self.vcmi.stream_logs()
