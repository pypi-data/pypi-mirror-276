import json
import os
import pathlib
import textwrap
from typing import Optional, TypedDict, Union

import click


class Config(TypedDict):
    python_version: str
    pip_config_file: Optional[str]
    dockerfile_lines: list[str]
    dependencies: list[str]
    graphs: dict[str, str]
    env: Union[dict[str, str], str]


def config_w_defaults(config: Config) -> Config:
    return {
        "python_version": config.get("python_version", "3.11"),
        "pip_config_file": config.get("pip_config_file"),
        "dockerfile_lines": config.get("dockerfile_lines", []),
        "dependencies": config.get("dependencies", []),
        "graphs": config.get("graphs", {}),
        "env": config.get("env", {}),
    }


def config_to_docker(config_path: pathlib.Path, config: Config):
    if config["python_version"] not in (
        "3.11",
        "3.12",
    ):
        raise click.UsageError(
            f"Unsupported Python version: {config['python_version']}. "
            "Supported versions are 3.11 and 3.12."
        )
    if not config["dependencies"]:
        raise click.UsageError(
            "No dependencies found in config."
            "Add at least one dependency to 'dependencies' list."
        )
    if not config["graphs"]:
        raise click.UsageError(
            "No graphs found in config."
            "Add at least one graph to 'graphs' dictionary."
        )

    pypi_deps = [dep for dep in config["dependencies"] if not dep.startswith(".")]
    local_pkgs: dict[pathlib.Path, str] = {}
    faux_pkgs: dict[pathlib.Path, str] = {}
    faux_pkg_has_requirements: set[str] = set()
    pkg_names = set()
    # if . is in dependencies, use it as working_dir
    working_dir = None
    pip_install = "pip install -c /api/constraints.txt"
    if config.get("pip_config_file"):
        pip_install = f"PIP_CONFIG_FILE=/pipconfig.txt {pip_install}"

    for local_dep in config["dependencies"]:
        if local_dep.startswith("."):
            resolved = config_path.parent / local_dep

            # validate local dependency
            if not resolved.exists():
                raise FileNotFoundError(f"Could not find local dependency: {resolved}")
            elif not resolved.is_dir():
                raise NotADirectoryError(
                    f"Local dependency must be a directory: {resolved}"
                )
            elif resolved.name in pkg_names:
                raise ValueError(f"Duplicate local dependency: {resolved}")
            else:
                pkg_names.add(resolved.name)

            # if it's installable, add it to local_pkgs
            # otherwise, add it to faux_pkgs, and create a pyproject.toml
            files = os.listdir(resolved)
            if "pyproject.toml" in files:
                local_pkgs[resolved] = local_dep
                if local_dep == ".":
                    working_dir = f"/deps/{resolved.name}"
            elif "setup.py" in files:
                local_pkgs[resolved] = local_dep
                if local_dep == ".":
                    working_dir = f"/deps/{resolved.name}"
            else:
                faux_pkgs[resolved] = local_dep
                if local_dep == ".":
                    working_dir = f"/deps/__outer_{resolved.name}/{resolved.name}"
                # if it has a requirements.txt,
                # - install its dependencies
                # - if package has __init__.py, skip subdirectories
                # - add any subdirectories with .py files to faux_pkgs
                if "requirements.txt" in files:
                    faux_pkg_has_requirements.add(local_dep)
                    if any(file == "__init__.py" for file in files):
                        continue
                    for file in files:
                        rfile = resolved / file
                        if rfile.is_dir():
                            for subfile in os.listdir(rfile):
                                if subfile.endswith(".py"):
                                    faux_pkgs[rfile] = file
                                    break

    for graph_id, import_str in config["graphs"].items():
        module_str, _, attr_str = import_str.partition(":")
        if not module_str or not attr_str:
            message = (
                'Import string "{import_str}" must be in format "<module>:<attribute>".'
            )
            raise ValueError(message.format(import_str=import_str))
        if "/" in module_str:
            resolved = config_path.parent / module_str
            if not resolved.exists():
                raise FileNotFoundError(f"Could not find local module: {resolved}")
            elif not resolved.is_file():
                raise IsADirectoryError(f"Local module must be a file: {resolved}")
            else:
                for local_pkg in local_pkgs:
                    if resolved.is_relative_to(local_pkg):
                        module_str = (
                            f"/deps/{local_pkg.name}/{resolved.relative_to(local_pkg)}"
                        )
                        break
                else:
                    for faux_pkg in faux_pkgs:
                        if resolved.is_relative_to(faux_pkg):
                            module_str = f"/deps/__outer_{faux_pkg.name}/{resolved.relative_to(faux_pkg.parent)}"
                            break
                    else:
                        raise ValueError(
                            f"Module '{import_str}' not found in 'dependencies' list"
                            "Add its containing package to 'dependencies' list."
                        )
            # update the config
            config["graphs"][graph_id] = f"{module_str}:{attr_str}"

    # https://setuptools.pypa.io/en/latest/userguide/datafiles.html#package-data
    # https://til.simonwillison.net/python/pyproject
    # if we ever want to include all non .py files without -e install
    # we can use the following pyproject.toml instead of empty one below
    """
    COPY <<EOF /deps/__outer_{fullpath.name}/pyproject.toml
    [project]
    name = "{fullpath.name}"
    version = "0.1"
    [tool.setuptools.package-data]
    {fullpath.name} = ["**/*"]
    EOF
    """
    pip_pkgs_str = f"RUN {pip_install} {' '.join(pypi_deps)}" if pypi_deps else ""
    faux_pkgs_str = f"{os.linesep}{os.linesep}".join(
        f"""ADD {relpath} /deps/__outer_{fullpath.name}/{fullpath.name}
RUN touch /deps/__outer_{fullpath.name}/pyproject.toml"""
        + (
            f"{os.linesep}RUN {pip_install} -r /deps/__outer_{fullpath.name}/{fullpath.name}/requirements.txt"
            if relpath in faux_pkg_has_requirements
            else ""
        )
        for fullpath, relpath in faux_pkgs.items()
    )
    local_pkgs_str = os.linesep.join(
        f"ADD {relpath} /deps/{fullpath.name}"
        for fullpath, relpath in local_pkgs.items()
    )
    pip_config_file_str = (
        f"ADD {config['pip_config_file']} /pipconfig.txt"
        if config.get("pip_config_file")
        else ""
    )

    return f"""FROM langchain/langgraph-api:{config['python_version']}

{os.linesep.join(config["dockerfile_lines"])}

{pip_config_file_str}

{pip_pkgs_str}

{local_pkgs_str}

{faux_pkgs_str}

RUN {pip_install} -e /deps/*

ENV LANGSERVE_GRAPHS='{json.dumps(config["graphs"])}'

{f"WORKDIR {working_dir}" if working_dir else ""}"""


def config_to_compose(
    config_path: pathlib.Path,
    config: Config,
    watch: bool = False,
    langgraph_api_path: Optional[pathlib.Path] = None,
):
    env_vars = config["env"].items() if isinstance(config["env"], dict) else {}
    env_vars_str = "\n".join(f"            {k}: {v}" for k, v in env_vars)
    env_file_str = (
        f"env_file: {config['env']}" if isinstance(config["env"], str) else ""
    )
    if watch:
        watch_paths = [config_path] + [
            config_path.parent / dep
            for dep in config["dependencies"]
            if dep.startswith(".")
        ]
        watch_actions = "\n".join(
            f"""- path: {path}
  action: rebuild
  ignore:
    - .langgraph-data"""
            for path in watch_paths
        )
        if langgraph_api_path:
            watch_actions += f"""\n- path: {langgraph_api_path}
  action: sync+restart
  target: /api/langgraph_api"""
        watch_str = f"""
        develop:
            watch:
{textwrap.indent(watch_actions, "                ")}
"""
    else:
        watch_str = ""

    return f"""
{textwrap.indent(env_vars_str, "            ")}
        {env_file_str}
        pull_policy: build
        build:
            context: .
            dockerfile_inline: |
{textwrap.indent(config_to_docker(config_path, config), "                ")}
        {watch_str}
"""
