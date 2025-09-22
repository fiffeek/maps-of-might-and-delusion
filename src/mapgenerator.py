from ai import AI

from logger import logger


class MapGenerator:
    def __init__(self, ai: AI) -> None:
        self.ai = ai

    def generate(self, seed: int):
        map_template = self.ai.start(seed=seed)
        logger.debug(
            map_template.model_dump_json(indent=2, exclude_none=True, by_alias=True)
        )
        pass
