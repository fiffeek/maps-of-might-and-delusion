from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
import pydantic_core

from disk_cache import DiskCache
from logger import logger
from models import (
    MapSize,
    MapTemplate,
    ModelResponseUnion,
)


class AI:
    def __init__(self, cache: DiskCache) -> None:
        self.model = AnthropicModel("claude-sonnet-4-20250514")
        self.agent = Agent(self.model, output_type=ModelResponseUnion)
        self.cache = cache

    def start(self, seed: int) -> MapTemplate:
        prompt = self.get_initial_prompt(seed)
        return self.__ask(prompt)

    def __ask(self, prompt: str) -> MapTemplate:
        cached_response = self.cache.get(prompt)
        if cached_response:
            logger.debug(f"Using cached response: {cached_response}")
            result = MapTemplate.model_validate(
                pydantic_core.from_json(cached_response)
            )
            logger.debug(
                f"Using cached response: {result.model_dump_json(indent=2, by_alias=True, exclude_none=True)}"
            )
            return result

        agent_result = self.agent.run_sync(prompt)
        result = MapTemplate.model_validate(agent_result.output)
        logger.debug(
            f"AI initially responded with: {result.model_dump_json(by_alias=True, exclude_none=True)}, usage: {agent_result.usage()}"
        )
        self.cache.upsert(
            prompt,
            pydantic_core.to_json(result, by_alias=True, exclude_none=True).decode(
                "utf-8"
            ),
        )
        logger.debug("Saved to cache")
        return result

    def get_initial_prompt(self, seed: int):
        map_size = MapSize.S
        players: int = 2
        prompt = f"""
Your high level goal is to generate a heroes of might and magic 3 map.
For this initial prompt respond with "MapTemplate".
Come up with a comprehensive map scenario, design the players starting zones, progression zones and end-game zones.
Fill in the map with as many zones as possible.
Design different maps for different seeds.
Requirement:
    - Map size: {map_size}
    - players: {players}
    - seed: {seed}
"""
        logger.debug(f"Prompt {prompt}")
        return prompt
