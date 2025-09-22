from typing import Optional
import yaml
from pydantic import BaseModel, Field

from file import os_expand
from models import MapSize


class Config(BaseModel):
    llm_model: str = Field(
        description="The LLM model to use to generate the output with (pydantic AI), requires the correct env var with the token.",
        default="anthropic:claude-sonnet-4-20250514",
    )
    llm_seed: int = Field(default=42, description="The generation seed for the LLM.")
    map_seed: int = Field(
        default=42, description="The generation seed for the map generation in VCMI."
    )
    save_path: str = Field(
        default="$HOME/.local/share/vcmi/Mods/momd/",
        description="The path to save the generated template with mod info to.",
    )
    players: int = Field(
        description="The expected minimum number of total players", ge=2
    )
    human: int = Field(
        description="The expected minimum number of human players", ge=1, alias="humans"
    )
    map_size: MapSize = Field(description="The size of the map.")
    freeform: Optional[str] = Field(
        default=None, description="Freeform text to define map specifics."
    )
    llm_retries: int = Field(
        description="The number of retries for the LLM in case it outputs non-compliant spec.",
        default=1,
    )

    def expand(self):
        self.save_path = os_expand(self.save_path)


def load(path: str) -> Config:
    with open(path, "r") as f:
        lines = f.readlines()
        content = "\n".join(lines)
        config_yaml = yaml.safe_load(content)
        config = Config.model_validate(config_yaml)
        config.expand()
        return config
