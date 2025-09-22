import json
import os
from typing import List
from ai import AI

from file import ensure_dir_exists, write_file
from logger import logger
from models import MapTemplate, MapTemplatesWrapper, VCMITemplatesMod


class MapGenerator:
    def __init__(self, ai: AI) -> None:
        self.ai = ai

    def generate(self, seed: int, save_directory: str):
        map_template = self.ai.start(seed=seed)
        map_template_json = map_template.model_dump_json(
            indent=2, exclude_none=True, by_alias=True
        )
        logger.debug(map_template_json)
        self.save_template(map_template, save_directory)

    def save_template(self, map_template: MapTemplate, save_directory: str):
        file = f"{save_directory}/content/{map_template.id}.JSON"
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
        self.save_mod(save_directory, files)

    def save_mod(self, save_directory: str, files: List[str]):
        ensure_dir_exists(save_directory)
        mod_file = f"{save_directory}/mod.json"
        write_file(
            mod_file,
            VCMITemplatesMod.new(files).model_dump_json(
                indent=2, exclude_none=True, by_alias=True
            ),
        )
