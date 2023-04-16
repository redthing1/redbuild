#!/usr/bin/env python3

import sh
import typer

from sh import python

PACKAGE_NAME = "redbuild"


def cli():
    nuitka_cmd = python.bake(
        "-m",
        "nuitka",
        "--standalone",
        "--onefile",
        "--python-flag=-m",
        f"{PACKAGE_NAME}",
        # f"--output-filename={PACKAGE_NAME}",
        _fg=True,
    )
    print(nuitka_cmd)
    nuitka_cmd()


def main():
    typer.run(cli)


if __name__ == "__main__":
    main()
