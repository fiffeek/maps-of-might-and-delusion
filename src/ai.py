from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
import pydantic_core

from disk_cache import DiskCache
from logger import logger
from models import GenerateMapResponse, MapSize, get_map_dimensions


class AI:
    def __init__(self, cache: DiskCache) -> None:
        self.model = AnthropicModel("claude-sonnet-4-20250514")
        self.agent = Agent(self.model, output_type=GenerateMapResponse)
        self.cache = cache

    def generate_map(self, seed: int) -> GenerateMapResponse:
        prompt = self.get_initial_prompt(seed)
        result = self.ask(prompt)
        logger.debug(f"Response: {result}")
        return result

    def ask(self, prompt: str):
        cached_response = self.cache.get(prompt)
        if cached_response:
            logger.debug("Using cached response")
            result = GenerateMapResponse.model_validate(
                pydantic_core.from_json(cached_response)
            )
            return result

        agent_result = self.agent.run_sync(prompt)
        result = GenerateMapResponse.model_validate(agent_result.output)
        self.cache.upsert(prompt, pydantic_core.to_json(result).decode("utf-8"))
        logger.debug("Saved to cache")
        return result

    def get_initial_prompt(self, seed: int):
        map_size = MapSize.S
        players: int = 4
        prompt = f"""
Generate a HOMM3 map according to the output spec.
Map size is: {map_size}, dimensions: {get_map_dimensions(map_size)}.
Players count: {players}.
Respect seeds, for different seeds give different maps.
Generation seed: {seed}.

The zones must occupy the entire map.
Be creative with the zones, they can consist of multiple shapes.
Make the zones as interesting in shape as possible, combine multiple smaller shapes to achieve best results.
Each zone should consist at least 4 shapes.
Everything left out will be water.
Do not output overlapping shapes for zones.
Cover the entire map with all the shapes.
The combined shapes of the zones should look interesting to the player.
Most zones should connect unless the map scenario says otherwise.
Keep in mind fairness of the players, they need reasonable starting zones.
"""
        logger.debug(f"Prompt {prompt}")
        return prompt
