#!/usr/bin/env python3

"""
redbuild
"""

import toml
import sh
import sys
import os
import typer
import multiprocessing
import psutil
from loguru import logger

from .engine import (
    ContainerEngine,
    detect_container_engine,
    get_container_engine_command,
)
from .util import get_builder_image_name

app = typer.Typer(
    name="redbuild",
    help="redbuild is a tool for easy magic containerized builds",
    no_args_is_help=True,
)


@app.command()
def info():
    host_os = sys.platform
    host_arch = sys.maxsize > 2**32 and "64bit" or "32bit"
    host_cores = multiprocessing.cpu_count()
    host_memory = int(psutil.virtual_memory().total / 1024**2)
    print(f"Host OS: {host_os}")
    print(f"Host architecture: {host_arch}")
    print(f"Host cores: {host_cores}")
    print(f"Host memory: {host_memory} MB")

    container_engine = detect_container_engine()
    print(f"Container engine: {container_engine}")


# build the build environment image
@app.command()
def image(
    dockerfile: str = typer.Option(
        "build.docker",
        "--dockerfile",
        "-f",
        help="Dockerfile to use for defining the build environment",
    ),
    cwd: str = typer.Option(
        ".", "--cwd", "-C", help="Directory to use as the build context"
    ),
):
    # 0. get container engine
    ctr_engine = get_container_engine_command(detect_container_engine())
    # 1. get name for builder image
    builder_image_name = get_builder_image_name(cwd)

    # full path to dockerfile
    dockerfile = os.path.join(cwd, dockerfile)

    # 2. build builder image
    # ensure dockerfile exists
    if not os.path.isfile(dockerfile):
        raise Exception(
            f"Dockerfile {dockerfile} not found. Create it or pass a specific path with -f."
        )

    # $CONTAINER_ENGINE build -t $BUILDER_TAG $CBUILD_ARGS -f $DOCKERFILE | sed 's/^/  /'
    print(f"Building builder image [{builder_image_name}] in context [{cwd}]:")
    build_cmd = ctr_engine.bake(
        "build",
        cwd,
        # podman build args
        t=builder_image_name,
        f=dockerfile,
        # _fg=True,
        # output formatting
        _out=lambda line: print(f"  {line}", end=""),
        _err=lambda line: print(f"  {line}", end=""),
    )

    logger.debug(f"Running command: {build_cmd}")
    build_proc = build_cmd()


@app.command()
def build(
    dockerfile: str = typer.Option(
        "build.docker",
        "--dockerfile",
        "-f",
        help="Dockerfile to use for defining the build environment",
    ),
    buildscript: str = typer.Option(
        "build.sh", "--buildscript", "-s", help="Build script to run in the container"
    ),
    cwd: str = typer.Option(
        ".", "--cwd", "-C", help="Directory to use as the build context"
    ),
    crun_args=typer.Option(
        "",
        "--crun-args",
        "-R",
        help="Additional arguments to pass to container engine",
    ),
):
    # 0. get container engine
    ctr_engine = get_container_engine_command(detect_container_engine())

    # 1. get name for builder image
    builder_image_name = get_builder_image_name(cwd)

    # 2. build builder image
    image(dockerfile=dockerfile, cwd=cwd)

    # 3. run build
    # $CONTAINER_ENGINE run --rm -it -v $(pwd):/prj $CRUN_ARGS $BUILDER_TAG /bin/bash -l -c "cd /prj && $BUILDSCRIPT $ARGS" | sed 's/^/  /'
    print(
        f"Running build in [{builder_image_name}] with buildscript [{buildscript}] in context [{cwd}]:"
    )
    run_cmd_args = [
        "run",
        # podman run args
        "--rm",
        # "-it",
        "-v",
        f"{cwd}:/prj",
        *[arg for arg in crun_args.split(" ") if arg],
    ]
    run_cmd = ctr_engine.bake(
        *run_cmd_args,
        # _fg=True,
        # output formatting
        _out=lambda line: print(f"  {line}", end=""),
        _err=lambda line: print(f"  {line}", end=""),
    )

    relative_buildscript = f"./{buildscript}"
    logger.debug(f"Running command: {run_cmd}")
    run_proc = run_cmd(
        builder_image_name,
        "/bin/bash",
        "-l",
        "-c",
        f"cd /prj && {relative_buildscript}",
    )


@app.callback()
def app_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    # loguru setup
    logger.remove()
    if verbose:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="INFO")


def main():
    app()
