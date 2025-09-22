import json
import os
from typing import List
from ai import AI

from config import Config
from file import write_file
from logger import logger
from models import MapTemplate, MapTemplatesWrapper, VCMITemplatesMod


class MapGenerator:
    def __init__(self, ai: AI, config: Config) -> None:
        self.ai = ai
        self.config = config

    def generate(self):
        map_template = self.ai.start()
        map_template_json = map_template.model_dump_json(
            indent=2, exclude_none=True, by_alias=True
        )
        logger.debug(map_template_json)
        self.save_template(map_template)

    def save_template(self, map_template: MapTemplate):
        file = f"{self.config.save_path}/content/{map_template.id}.JSON"
        logger.debug(f"Saving to file {file}")
        wrapper = MapTemplatesWrapper.new(templates=[map_template])
        map_template_dict = wrapper.model_dump(
            exclude_none=True,
            by_alias=True,
        )
        for _, val in map_template_dict.items():
            val.pop("kind")
            val.pop("id")
            for _, zone in val["zones"].items():
                zone.pop("id")
        map_template_json = json.dumps(map_template_dict)
        logger.debug(f"Writing {map_template_json} to file.")
        write_file(file, map_template_json)
        files = [os.path.basename(file) for file in os.listdir(os.path.dirname(file))]
        self.save_mod(files)

    def save_mod(self, files: List[str]):
        mod_file = f"{self.config.save_path}/mod.json"
        write_file(
            mod_file,
            VCMITemplatesMod.new(files).model_dump_json(
                indent=2, exclude_none=True, by_alias=True
            ),
        )
