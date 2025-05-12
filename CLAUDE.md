# claude.md

this file provides guidance to claude code (claude.ai/code) when working with code in this repository.

## project overview

redbuild is a tool for containerized builds that helps users define and execute builds in isolated environments. it uses containerization (via podman or docker) to create reproducible build environments for projects.

## commands

### building redbuild from source

to build redbuild itself:

```sh
# bootstrap build environment and compile redbuild
./bootstrap/redbuild.sh

# this produces redbuild.bin which can be symlinked to your path
mkdir -p ~/.bin
ln -s $(pwd)/redbuild.bin ~/.bin/redbuild
```

for development:

```sh
# install dependencies with poetry
poetry install

# run redbuild in development mode
poetry run python -m redbuild [command]

# build native binary
poetry run python script/build_native.py
```

### using redbuild

commands for using the redbuild tool:

```sh
# show redbuild version and information
redbuild info

# initialize a build environment in the current directory
redbuild init
redbuild init --wizard  # interactive configuration

# build the container image for the build environment
redbuild image

# run the build script in the container
redbuild build 

# open a shell in the build environment
redbuild shell

# get help with any command
redbuild --help
redbuild [command] --help  # e.g., redbuild build --help
```

## architecture

redbuild's architecture consists of:

1. **cli interface** (`cli.py`): main entry point that handles command-line arguments and subcommands.

2. **container engine** (`engine.py`): abstracts container operations, detecting and interfacing with either podman or docker.

3. **dockerfile composer** (`composer.py`): handles generation of dockerfile templates for build environments.

4. **utilities** (`util.py`): helper functions for image naming and argument parsing.

the workflow is:
1. define a build environment with a `build.docker` file
2. create a build script (`build.sh`) to execute in the environment
3. use redbuild to build the image and run the build script in the container

## development notes

- redbuild prefers podman over docker but will use docker if podman is not available
- build artifacts are placed in the host's project directory via volume mounts
- the build environment is defined by a dockerfile (default: `build.docker`)
- the build script (default: `build.sh`) executes the actual build commands inside the container

## python code style guide

- write well-organized, high-quality, self-documenting code
- use standard naming conventions: UpperCamelCase for types, snake_case for variables, functions, etc.; keep acronyms capitalized
- use lowercase comments: `# always like this`
- write detailed explanatory comments to document anything complex. especially for things that are confusing, technically complex, or require specific domain knowledge that isn't obvious or clear, always document this in depth so that a reader can understand and/or get up to speed on concepts
- comments should generally be on their own line preceding the thing; don't put comments on the same line
- avoid writing slop comments explaining _changes_ to the code when writing code; do your thought process before you write code, and write the code itself. don't write meta-comments explaining your changes to the code, just write high-quality self-documenting code
- don't write comments like `# --- whatever`; generally just write them like `# this`, or if you need a category/heading/group then `# - group description`
- when given a single python file to edit that imports modules/functions, relative or absolute, assume they are available (we just might be editing only one file at once)