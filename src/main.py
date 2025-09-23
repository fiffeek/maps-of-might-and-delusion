import click
from app import App
from logger import setup_logging


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.pass_context
def main(ctx, debug: bool):
    setup_logging(debug)
    ctx.ensure_object(dict)


@main.command()
@click.option(
    "--config-path",
    help="Path to the configuration of the generation engine",
    required=True,
)
@click.option(
    "--cache",
    help="Path to save the LLM responses to.",
    default="$XDG_CACHE_HOME/aiomad/responses",
)
@click.pass_context
def generate(
    ctx,
    config_path: str,
    cache: str,
):
    app = App(
        cache_path=cache,
        config_path=config_path,
    )
    app.generate_map()


if __name__ == "__main__":
    main()
