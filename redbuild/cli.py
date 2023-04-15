#!/usr/bin/env python3

"""
redbuild
"""

import toml
import sh
import sys
import typer
import multiprocessing
import psutil
from loguru import logger

from .engine import (
    ContainerEngine,
    detect_container_engine,
    get_container_engine_command,
)

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
