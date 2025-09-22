import pathlib
from jinja2 import Environment, FileSystemLoader

from config import Config


class Templates:
    def __init__(self, config: Config) -> None:
        parent = pathlib.Path(__file__).parent.resolve()
        self.env = Environment(loader=FileSystemLoader(parent / "templates"))
        self.template = self.env.get_template("initial_prompt.j2")
        self.config = config

    def get_initial_prompt(self):
        output = self.template.render(
            seed=self.config.llm_seed,
            map_size=self.config.map_size,
            players=self.config.players,
            humans=self.config.human,
            freeform=self.config.freeform,
        )
        return output
