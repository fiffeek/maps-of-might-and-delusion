import pathlib
import click
from app import StandaloneVCMI, VCMIGeneratorApp
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
    "--xauth-dir",
    help="Path to where to generate the xauth file to",
    default=pathlib.Path(__file__).parent.parent.resolve() / "xauth",
)
@click.option(
    "--cache",
    help="Path to save the LLM responses to.",
    default="$XDG_CACHE_HOME/aiomad/responses",
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
    "--homm-data-path",
    help="Path to the homm3 data",
    required=True,
)
@click.option(
    "--xauth-dir",
    help="Path to where to generate the xauth file to",
    default=pathlib.Path(__file__).parent.parent.resolve() / "xauth",
)
@click.option(
    "--display",
    help="X display to create",
    default=42,
)
@click.pass_context
def generate(
    ctx,
    config_path: str,
    homm_data_path: str,
    repository: str,
    tag: str,
    display: int,
    xauth_dir: str,
    cache: str,
):
    app = VCMIGeneratorApp(
        cache_path=cache,
        homm_data_path=homm_data_path,
        repository=repository,
        tag=tag,
        display=display,
        xauth_dir=xauth_dir,
        config_path=config_path,
    )
    app.generate_map()


@main.command()
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
    "--homm-data-path",
    help="Path to the homm3 data",
    required=True,
)
@click.option(
    "--xauth-dir",
    help="Path to where to generate the xauth file to",
    default=pathlib.Path(__file__).parent.parent.resolve() / "xauth",
)
@click.option(
    "--display",
    help="X display to create",
    default=42,
)
@click.pass_context
def standalone_vcmi(
    ctx, homm_data_path: str, repository: str, tag: str, display: int, xauth_dir: str
):
    app = StandaloneVCMI(
        homm_data_path=homm_data_path,
        repository=repository,
        tag=tag,
        display=display,
        xauth_dir=xauth_dir,
    )
    app.run_standalone_vcmi()


if __name__ == "__main__":
    main()
