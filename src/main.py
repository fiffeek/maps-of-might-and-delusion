import click
import docker
from app import Application
from logger import setup_logging, logger
from vcmi import VCMI


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
@click.pass_context
def main(ctx, debug: bool, homm_data_path: str, repository, tag, display, xauth_dir):
    setup_logging(debug)
    ctx.ensure_object(dict)
    ctx.obj["homm_data_path"] = homm_data_path
    ctx.obj["repository"] = repository
    ctx.obj["tag"] = tag
    ctx.obj["display"] = display
    ctx.obj["xauth_dir"] = xauth_dir


@main.command()
@click.option(
    "--cache",
    help="Path to save the LLM responses to.",
    default="$XDG_CACHE_HOME/aiomad/responses",
)
@click.option(
    "--seed",
    help="A seed for map generation",
    default=1,
)
@click.pass_context
def generate(ctx, cache: str, seed: int):
    homm_data_path = ctx.obj["homm_data_path"]
    repository = ctx.obj["repository"]
    display = ctx.obj["display"]
    tag = ctx.obj["tag"]
    xauth_dir = ctx.obj["xauth_dir"]
    app = Application(
        cache_path=cache,
        homm_data_path=homm_data_path,
        repository=repository,
        tag=tag,
        display=display,
        xauth_dir=xauth_dir,
    )
    app.generate_map(seed)


@main.command()
@click.pass_context
def standalone_vcmi(ctx):
    homm_data_path = ctx.obj["homm_data_path"]
    repository = ctx.obj["repository"]
    display = ctx.obj["display"]
    tag = ctx.obj["tag"]
    xauth_dir = ctx.obj["xauth_dir"]
    client = docker.from_env()

    logger.info("Starting vcmi")
    with VCMI(
        repository=repository,
        tag=tag,
        docker_client=client,
        display=display,
        homm_data_path=homm_data_path,
        xauth_mount_dir=xauth_dir,
    ) as vcmi:
        vcmi.stream_logs()
        logger.info("Stopping vcmi")


if __name__ == "__main__":
    main()
