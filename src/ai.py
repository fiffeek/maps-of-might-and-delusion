from typing import Optional
from pydantic import TypeAdapter
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
import pydantic_core

from disk_cache import DiskCache
from logger import logger
from models import (
    CodeResponse,
    CreateMapRequest,
    MapSize,
    ModelResponse,
    ModelResponseUnion,
    get_map_dimensions,
)


class AI:
    def __init__(self, cache: DiskCache) -> None:
        self.model = AnthropicModel("claude-sonnet-4-20250514")
        self.agent = Agent(self.model, output_type=ModelResponseUnion)
        self.cache = cache

    def start(self, seed: int) -> CreateMapRequest:
        prompt = self.get_initial_prompt(seed)
        return self.__ask(prompt)

    def __ask(self, prompt: str) -> CreateMapRequest:
        cached_response = self.cache.get(prompt)
        if cached_response:
            logger.debug("Using cached response")
            result = CreateMapRequest.model_validate(
                pydantic_core.from_json(cached_response)
            )
            logger.debug(f"Using cached response: {result.model_dump_json(indent=2)}")
            return result

        agent_result = self.agent.run_sync(prompt)
        result = CreateMapRequest.model_validate(agent_result.output)
        logger.debug(
            f"AI initially responded with: {result.model_dump_json()}, usage: {agent_result.usage()}"
        )
        self.cache.upsert(prompt, pydantic_core.to_json(result).decode("utf-8"))
        logger.debug("Saved to cache")
        return result

    def get_action(self, code_response: Optional[CodeResponse]) -> ModelResponse:
        prompt = self.get_continuation_prompt(code_response)
        logger.debug(f"Responding to agent with {prompt}")
        result = self.agent.run_sync(prompt)
        ta = TypeAdapter(ModelResponse)
        model = ta.validate_python(result.output)
        logger.debug(
            f"AI responded with: {model.model_dump_json()}, usage: {result.usage()}"
        )
        return model

    def get_continuation_prompt(self, code_response: Optional[CodeResponse]) -> str:
        lines = []
        if code_response:
            lines.extend(
                [
                    f"Response to your previous action: {code_response.model_dump_json()}",
                    f"Expected next action: {code_response.next_action}",
                ]
            )
        lines.extend(
            [
                "If there is an error, please correct it, if not let's continue with the generation.",
            ]
        )
        return "\n".join(lines)

    def get_initial_prompt(self, seed: int):
        map_size = MapSize.S
        players: int = 2
        prompt = f"""
Your high level goal is to generate a heroes of might and magic 3 map.
We will do it collaboratevely, you should always respond to me with one of the actions from the output specification.
For this initial prompt respond with "CreateMapRequest".

To accomplish this:
    1. Examine the constraints from the output, and from the input prompt underneath.
    2. Come up with a creative scenario that will be fun to play for players.
    3. Create a high level plan that you will follow, e.g.:
        3.1 How many zones there would be, overall shape and their ids.
    3. Initially respond with "CreateMapRequest".
    4. You might be asked later to create or move objects, respond with the actions from the output spec.
Requirements:
    1. Map size is: {map_size}.
    2. Map dimensions in tiles is {get_map_dimensions(map_size)}.
    3. Expected player count is: {players}. Can be either computer or human.
    4. For different generation seeds give a different map. Current generation seed is {seed}.
    5. The zones must occupy the entire map.
    6. Zones must be connected in one way or another - either by underground, by portals, or by ships.
    7. Different zones should not overlap each other.
    8. Zones should be connected unless the specific user prompt says otherwise.
    9. Take into account the fairness of the game -- we want all players to have equal chances of winning,
       that means that the starting zones MUST be fair.
    10. Zone ids have to be unique.
    11. If there is an underground entrance, it should appear in the underground zone.
    12. For any underground entrance, a zone should exist on the surface and underground connecting them.
    13. For neutral towns prefer specific town types, for player owned towns prefer a random town.
    14. Where possible account for "dimensions" property that specify the dimensions of the object (anchored at the right bottom corner).
        Post processing is done to ensure no objects overlap but the better the spec itself the more consistent the map will be.
    15. If one player has access to a specific resource or building in the starting zone, then all the players should have similar resources in their starting zones.
        Similar applies to mid and late-game zones.
    16. Neutral resources should be available in similar proximity to all players, e.g. if there is a neutral town closer to one player than another then the game would not be balanced
        this can be mitigated either by placing the same resource multiple times or by placing it roughly in the same distance.
    17. Think about passability -- the players must be able to leave and explore other zones.
    18. Any town has to have ORE_PIT and SAWMILL relatively close to it.
    19. Any buildings and towns should be placed so that there is a little space between them (at least 1 tile).
    20. Shipyards or boats have to be placed on the perimiter of the zones that touch water.
    21. Maximize the space used by zones.
    22. Any castle should have a road leading up to it.
    23. For starting areas there should be a road between the ORE_PIT and the town; same for SAWMILL and the town.
    24. Use obstacles inteligently to block access to some resources. Lots of obstacles are expected.
    25. Obstacles should not be placed on rivers.
    26. Zones should have at least 4 shapes.
Constraints:
    1. Anything left out from the zones will be "water" on the surface and "rock" underground.
Hints:
    1. To make interesting zones, use multiple shapes.
    2. Shapes inside a specific zone can be overlapping.
    3. If it makes sense for the map to have underground, enable it and put zones there.
    4. The map does not have to be symmetric, just ensure some level of fairness.
"""
        logger.debug(f"Prompt {prompt}")
        return prompt
