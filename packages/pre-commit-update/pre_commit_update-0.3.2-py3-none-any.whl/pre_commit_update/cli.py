import os
import sys
from typing import Any, Dict, Tuple

import click

from .managers import EnvManager, MessageManager, RepoManager, YAMLManager
from .utils import (
    RepoType,
    get_color,
    get_dict_diffs,
    get_passed_params,
    get_toml_config,
)


def _preview(
    *, defaults: Dict, toml_params: Dict, cmd_params: Dict, final_params: Dict
) -> None:
    click.echo(get_color("Default configuration values:", "blue"))
    for k, v in defaults.items():
        click.echo(f"{k} = {v}")
    click.echo(
        get_color("\npyproject.toml configuration values (difference):", "yellow")
    )
    toml_diff: Dict = get_dict_diffs(defaults, toml_params)
    if toml_diff:
        for k, v in toml_diff.items():
            click.echo(f"{k} = {v}")
    else:
        click.echo("Same as the default configuration / no configuration found")
    click.echo(get_color("\nCommand line configuration values (difference):", "red"))
    cmd_diff: Dict = get_dict_diffs(toml_params, cmd_params)
    if cmd_diff:
        for k, v in cmd_diff.items():
            click.echo(f"{k} = {v}")
    else:
        click.echo("Same as the default configuration / pyproject.toml configuration")
    click.echo(get_color("\nFinal configuration values:", "green"))
    for k, v in final_params.items():
        click.echo(f"{k} = {v}")


def _run(
    *, dry_run: bool, all_versions: bool, verbose: bool, exclude: Tuple, keep: Tuple
) -> None:
    # Backup and set needed env variables
    env_manager: EnvManager = EnvManager()
    env_manager.setup()
    # Do the magic
    try:
        message_manager: MessageManager = MessageManager()
        yaml_manager: YAMLManager = YAMLManager(
            os.path.join(os.getcwd(), ".pre-commit-config.yaml")
        )
        repo_manager: RepoManager = RepoManager(
            yaml_manager.data["repos"], all_versions, exclude, keep
        )
        repo_manager.get_updates(message_manager)

        if message_manager.warning:
            message_manager.output_messages(message_manager.warning)

        if verbose:
            for output in (
                message_manager.excluded,
                message_manager.kept,
                message_manager.no_update,
            ):
                if not output:
                    continue
                message_manager.output_messages(output)

        if message_manager.to_update:
            message_manager.output_messages(message_manager.to_update)

            if dry_run:
                raise click.ClickException(get_color("Changes detected", "red"))

            yaml_manager.data["repos"] = repo_manager.repos_data
            yaml_manager.dump()
            click.echo(get_color("Changes detected and applied", "green"))
            return

        click.echo(get_color("No changes detected", "green"))

    except Exception as ex:
        sys.exit(str(ex))

    finally:
        # Restore env variables
        env_manager.restore()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-d/-nd",
    "--dry-run/--no-dry-run",
    is_flag=True,
    show_default=True,
    default=False,
    help="Dry run only checks for the new versions without updating",
)
@click.option(
    "-a/-na",
    "--all-versions/--no-all-versions",
    is_flag=True,
    show_default=True,
    default=False,
    help="Include the alpha/beta versions when updating",
)
@click.option(
    "-v/-nv",
    "--verbose/--no-verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Display the complete output",
)
@click.option(
    "-p/-np",
    "--preview/--no-preview",
    is_flag=True,
    show_default=True,
    default=False,
    help="Previews the cli configuration values by overwriting order (disables the actual cli work if enabled!)",
)
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    type=RepoType(),
    default=(),
    help="Exclude specific repo(s) by the `repo` url trim",
)
@click.option(
    "-k",
    "--keep",
    multiple=True,
    type=RepoType(),
    default=(),
    help="Keep the version of specific repo(s) by the `repo` url trim (still checks for the new versions)",
)
@click.pass_context
def cli(ctx: click.Context, **_: Any):
    defaults: Dict = {
        p.name: list(p.default) if isinstance(p.default, tuple) else p.default
        for p in ctx.command.params
    }
    toml_params: Dict = get_toml_config(defaults)
    cmd_params: Dict = get_passed_params(ctx)
    final_params: Dict = {**toml_params, **cmd_params}

    if final_params["preview"]:
        _preview(
            defaults=defaults,
            toml_params=toml_params,
            cmd_params=cmd_params,
            final_params=final_params,
        )
        return

    final_params.pop("preview")
    _run(**final_params)


if __name__ == "__main__":
    cli()
