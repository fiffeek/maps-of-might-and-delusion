import click
from app import Application
from logger import setup_logging


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option(
    "--homm-data-path",
    help="Path to the homm3 data",
    required=True,
)
@click.option(
    "--xauth-dir",
    help="Path to where to generate the xauth file to",
    required=True,
)
@click.option(
    "--repository",
    help="Docker image repository",
    default="vcmi",
)
@click.option(
    "--tag",
    help="Docker image tag",
    default="dev",
)
@click.option(
    "--display",
    help="X display to create",
    default=42,
)
@click.option(
    "--cache",
    help="Path to save the LLM responses to.",
    default="$XDG_CACHE_HOME/aiomad/responses",
)
@click.pass_context
def main(
    ctx, debug: bool, homm_data_path: str, repository, tag, display, xauth_dir, cache
):
    setup_logging(debug)
    ctx.ensure_object(dict)
    ctx.obj["app"] = Application(
        cache_path=cache,
        homm_data_path=homm_data_path,
        repository=repository,
        tag=tag,
        display=display,
        xauth_dir=xauth_dir,
    )


@main.command()
@click.option(
    "--seed",
    help="A seed for map generation",
    default=1,
)
@click.pass_context
def generate(ctx, seed: int):
    app: Application = ctx.obj["app"]
    app.generate_map(seed)


@main.command()
@click.pass_context
def standalone_vcmi(ctx):
    app: Application = ctx.obj["app"]
    app.run_standalone_vcmi()


if __name__ == "__main__":
    main()
