import logging
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Optional

import click

import tecton
from tecton import conf
from tecton import tecton_context
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton._internals.utils import cluster_url
from tecton.cli import access_control
from tecton.cli import api_key
from tecton.cli import auth
from tecton.cli import completion
from tecton.cli import engine
from tecton.cli import environment
from tecton.cli import materialization
from tecton.cli import plan
from tecton.cli import printer
from tecton.cli import repo
from tecton.cli import repo_config
from tecton.cli import secrets
from tecton.cli import service_account
from tecton.cli import test
from tecton.cli import user
from tecton.cli import workspace
from tecton.cli.command import TectonGroup
from tecton.cli.engine import dump_local_state
from tecton.cli.repo_utils import get_tecton_objects
from tecton.cli.workspace_utils import WorkspaceType


CONTEXT_SETTINGS = {
    "max_content_width": 160,
    "help_option_names": ["-h", "--help"],
}


@click.group(name="tecton", context_settings=CONTEXT_SETTINGS, cls=TectonGroup)
@click.option("--verbose", "-v", is_flag=True, help="Increase verbosity level to print more information.")
def cli(verbose: bool = False):
    """Tecton command-line tool."""
    sdk_decorators.disable_sdk_public_method_decorator()
    conf.enable_save_tecton_configs()

    logging_level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=logging_level,
        stream=sys.stderr,
        format="%(levelname)s(%(name)s): %(message)s",
    )

    # add cwd to path
    sys.path.append("")


cli.add_command(auth.login)
cli.add_command(auth.logout)
cli.add_command(auth.whoami)
cli.add_command(access_control.access_control)
cli.add_command(api_key.api_key)
cli.add_command(completion.completion)
cli.add_command(engine.apply)
cli.add_command(engine.destroy)
cli.add_command(engine.upgrade)
cli.add_command(environment.environment)
cli.add_command(materialization.materialization_status)
cli.add_command(materialization.freshness)
cli.add_command(repo.init)
cli.add_command(repo.restore)
cli.add_command(secrets.secrets)
cli.add_command(service_account.service_account)
cli.add_command(test.test)
cli.add_command(user.user)
cli.add_command(plan.plan)
cli.add_command(workspace.workspace)
cli.add_command(repo_config.repo_config_group)


@cli.command(requires_auth=False)
def version():
    """Print version."""
    tecton.version.summary()


@cli.command(hidden=True)
@click.option(
    "--config",
    help="Path to the repo config yaml file. Defaults to the repo.yaml file at the Tecton repo root.",
    default=None,
    type=click.Path(exists=True, dir_okay=False, path_type=Path, readable=True),
)
def dump(config: Optional[Path]) -> None:
    """Print the serialization format for object definitions in this repository.

    Useful for debugging issues related to serializing the Tecton repository to be sent to the Tecton backend.
    """
    # TODO(jake): get_tecton_objects prints out to stdout, which breaks piping the `tecton dump` output. Start printing
    # to stderr.
    top_level_objects, _, _, _ = get_tecton_objects(config)
    dump_local_state(top_level_objects)


@cli.command(uses_workspace=True, hidden=True)
@click.option("--limit", default=10, type=int, help="Number of log entries to return.")
def log(limit):
    """View log of applied plans in workspace"""
    # TODO: Remove before tecton version 1.1.0
    printer.safe_print()
    plan.list_impl(limit)


@cli.command()
@click.option(
    "--workspace",
    default=None,
    type=WorkspaceType(),
    help="The workspace page that should be opened up to. Defaults to the current selected workspace.",
)
@click.option(
    "--print/--no-print", "-p", "print_", default=False, help="Print the URL instead of automatically opening it."
)
def web(workspace, print_) -> None:
    """Opens a browser window to your Tecton account and workspace."""
    workspace_name = workspace if workspace else tecton_context.get_current_workspace()
    if workspace_name:
        web_url = urllib.parse.urljoin(cluster_url(), f"app/repo/{workspace_name}/")
    else:
        web_url = urllib.parse.urljoin(cluster_url(), "app")

    if print_:
        printer.safe_print(f"Web URL: {web_url}")
    else:
        printer.safe_print(f"Opening {web_url}")
        # Sleep before opening the browser to improve the UX and make it less jarring.
        time.sleep(1)
        click.launch(web_url)


def main():
    try:
        cli()
    finally:
        metadata_service.close_instance()


if __name__ == "__main__":
    main()
