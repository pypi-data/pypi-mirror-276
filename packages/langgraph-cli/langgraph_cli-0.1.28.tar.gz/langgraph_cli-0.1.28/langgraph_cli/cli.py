import asyncio
import json
import os
import pathlib
import shutil
import signal
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Coroutine, Iterable, Optional

import click

import langgraph_cli.config
import langgraph_cli.docker


async def exec(
    cmd: str, *args: str, input: Optional[str] = None, wait: Optional[float] = None
):
    if wait:
        await asyncio.sleep(wait)
    try:
        proc = await asyncio.create_subprocess_exec(
            cmd, *args, stdin=asyncio.subprocess.PIPE if input else None
        )
        await proc.communicate(input.encode() if input else None)
        if (
            proc.returncode is not None
            and proc.returncode != 0  # success
            and proc.returncode != 130  # user interrupt
        ):
            raise click.exceptions.Exit(proc.returncode)
    finally:
        try:
            if proc.returncode is None:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGINT)
                except (ProcessLookupError, KeyboardInterrupt):
                    pass
        except UnboundLocalError:
            pass


PLACEHOLDER_NOW = object()


async def exec_loop(cmd: str, *args: str, input: Optional[str] = None):
    now = datetime.now(timezone.utc).isoformat()
    while True:
        try:
            await exec(
                cmd, *(now if a is PLACEHOLDER_NOW else a for a in args), input=input
            )
            now = datetime.now(timezone.utc).isoformat()
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            pass


async def gather(*coros: Coroutine):
    tasks: Iterable[asyncio.Task] = [asyncio.create_task(coro) for coro in coros]
    exceptions = []
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for t in tasks:
            t.cancel()
        for d in done:
            if exc := d.exception():
                exceptions.append(exc)


OPT_O = click.option(
    "--docker-compose",
    "-d",
    help="Advanced: Path to docker-compose.yml file with additional services to launch",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
)
OPT_C = click.option(
    "--config",
    "-c",
    help="""Path to configuration file declaring dependencies, graphs and environment variables.
    
    \b
    Example:
    {
        "dependencies": [
            "langchain_openai",
            "./your_package"
        ],
        "graphs": {
            "my_graph_id": "./your_package/your_file.py:variable"
        },
        "env": "./.env"
    }

    Defaults to looking for langgraph.json in the current directory.""",
    default="langgraph.json",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
)
OPT_PORT = click.option(
    "--port", "-p", type=int, default=8123, show_default=True, help="Port to expose"
)
OPT_DEBUGGER_PORT = click.option(
    "--debugger-port",
    "-dp",
    type=int,
    default=8124,
    show_default=True,
    help="Port to expose debug UI on",
)
OPT_RECREATE = click.option(
    "--recreate/--no-recreate",
    default=False,
    show_default=True,
    help="Clear previous data",
)
OPT_PULL = click.option(
    "--pull/--no-pull", default=True, show_default=True, help="Pull latest images"
)


@click.group()
def cli():
    pass


@OPT_RECREATE
@OPT_PULL
@OPT_DEBUGGER_PORT
@OPT_PORT
@OPT_O
@OPT_C
@click.option("--watch", is_flag=True, help="Restart on file changes")
@click.option(
    "--langgraph-api-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    hidden=True,
)
@click.option(
    "--wait",
    is_flag=True,
    help="Wait for services to start before returning. Implies --detach",
)
@cli.command(help="Start langgraph API server")
def up(
    config: pathlib.Path,
    docker_compose: Optional[pathlib.Path],
    port: int,
    recreate: bool,
    pull: bool,
    debugger_port: Optional[int],
    watch: bool,
    langgraph_api_path: Optional[pathlib.Path],
    wait: bool,
):
    with Runner() as runner:
        args, stdin = prepare(
            runner,
            config=config,
            docker_compose=docker_compose,
            port=port,
            pull=pull,
            debugger_port=debugger_port,
            watch=watch,
            langgraph_api_path=langgraph_api_path,
        )
        # add up + options
        args.append("up")
        if recreate:
            args.extend(
                ["--force-recreate", "--remove-orphans", "--renew-anon-volumes"]
            )
            shutil.rmtree(".langgraph-data", ignore_errors=True)
        if watch:
            args.append("--watch")
        if wait:
            args.append("--wait")
        # run docker compose
        runner.run(exec("docker", "compose", *args, input=stdin))


@OPT_DEBUGGER_PORT
@OPT_PORT
@OPT_O
@OPT_C
@cli.command(help="Stop langgraph API server")
def down(
    config: pathlib.Path,
    docker_compose: Optional[pathlib.Path],
    port: int,
    debugger_port: Optional[int],
):
    with Runner() as runner:
        args, stdin = prepare(
            runner,
            config=config,
            docker_compose=docker_compose,
            port=port,
            pull=False,
            debugger_port=debugger_port,
            watch=False,
            langgraph_api_path=None,
        )
        # add down + options
        args.append("down")
        # run docker compose
        runner.run(exec("docker", "compose", *args, input=stdin))


@OPT_C
@OPT_PULL
@click.option("--tag", "-t", help="Tag for the image", required=True)
@click.option("--platform", help="Platform to build for")
@cli.command(help="Build langgraph API server docker image")
def build(
    config: pathlib.Path,
    platform: Optional[str],
    pull: bool,
    tag: str,
):
    with open(config) as f:
        config_json = langgraph_cli.config.config_w_defaults(json.load(f))
    with Runner() as runner:
        # check docker available
        try:
            runner.run(exec("docker", "--version"))
        except click.exceptions.Exit:
            click.echo("Docker not installed or not running")
            return
        # pull latest images
        if pull:
            runner.run(
                exec(
                    "docker",
                    "pull",
                    f"langchain/langgraph-api:{config_json['python_version']}",
                )
            )
        # apply options
        args = [
            "-f",
            "-",  # stdin
            "-t",
            tag,
        ]
        if platform:
            args.extend(["--platform", platform])
        # apply config
        stdin = langgraph_cli.config.config_to_docker(config, config_json)
        # run docker build
        runner.run(exec("docker", "build", *args, str(config.parent), input=stdin))


@OPT_DEBUGGER_PORT
@OPT_PORT
@OPT_O
@OPT_C
@cli.command(help="Build a helm chart to deploy to a Kubernetes cluster", hidden=True)
def helm(
    config: pathlib.Path,
    docker_compose: Optional[pathlib.Path],
    port: int,
    debugger_port: Optional[int],
):
    with open(config) as f:
        config_json = langgraph_cli.config.config_w_defaults(json.load(f))
    with Runner() as runner:
        # check docker available
        try:
            runner.run(exec("docker", "--version"))
            runner.run(exec("docker", "compose", "version"))
        except click.exceptions.Exit:
            click.echo("Docker not installed or not running")
            return
        # prepare args
        stdin = langgraph_cli.docker.compose(
            port=port,
            debugger_port=debugger_port,
            python_version=config_json["python_version"],
        )
        args = [
            "--chart",
            "-o=./helm",
            "-v",
            "-f",
            "-",  # stdin
        ]
        # apply options
        if docker_compose:
            args.extend(["-f", str(docker_compose)])
        args.append("convert")
        # apply config
        stdin += langgraph_cli.config.config_to_compose(config, config_json)
        # run kompose convert
        runner.run(exec("kompose", *args, input=stdin))


@contextmanager
def Runner():
    if hasattr(asyncio, "Runner"):
        with asyncio.Runner() as runner:
            yield runner
    else:

        class _Runner:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def run(self, coro):
                asyncio.run(coro)

        yield _Runner()


def prepare(
    runner,
    *,
    config: pathlib.Path,
    docker_compose: Optional[pathlib.Path],
    port: int,
    pull: bool,
    debugger_port: Optional[int],
    watch: bool,
    langgraph_api_path: Optional[pathlib.Path],
):
    with open(config) as f:
        config_json = langgraph_cli.config.config_w_defaults(json.load(f))
    # check docker available
    try:
        runner.run(exec("docker", "--version"))
        runner.run(exec("docker", "compose", "version"))
    except click.exceptions.Exit:
        click.echo("Docker not installed or not running")
        return
    # pull latest images
    if pull:
        runner.run(
            exec(
                "docker",
                "pull",
                f"langchain/langgraph-api:{config_json['python_version']}",
            )
        )
        runner.run(exec("docker", "pull", "langchain/langserve-debugger"))
    # prepare args
    stdin = langgraph_cli.docker.compose(
        port=port,
        debugger_port=debugger_port,
        python_version=config_json["python_version"],
    )
    args = [
        "--project-directory",
        config.parent,
        "-f",
        "-",  # stdin
    ]
    # apply config
    stdin += langgraph_cli.config.config_to_compose(
        config, config_json, watch=watch, langgraph_api_path=langgraph_api_path
    )
    # apply options
    if docker_compose:
        args.extend(["-f", str(docker_compose)])

    return args, stdin
