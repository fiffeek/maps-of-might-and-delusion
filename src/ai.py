from pydantic_ai import Agent
import pydantic_core

from disk_cache import DiskCache
from logger import logger
from models import (
    MapTemplate,
    ModelResponseUnion,
)
from templates import Templates
from config import Config


class AI:
    def __init__(self, cache: DiskCache, templates: Templates, config: Config) -> None:
        self.config = config
        self.agent = Agent(
            self.config.llm_model,
            output_type=ModelResponseUnion,
            retries=self.config.llm_retries,
        )
        self.cache = cache
        self.templates = templates

    def start(self) -> MapTemplate:
        prompt = self.templates.get_initial_prompt()
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
