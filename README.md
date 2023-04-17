
# redbuild

magic containerized builds

## overview

redbuild is a super simple drop-in script enabling software to be built in pre-defined containers. with `podman` installed, any supported project can be built with a single command. projects provide a `build.docker` and `build.sh` for defining the build environment and build steps.

`redbuild`: just add water!

## install stable version from pypi

```sh
# with pipx (recommended)
pipx install redbuild
# with vanilla pip
pip install redbuild
```

## build from source

To build redbuild2, we will use the redbuild1 shell script to bootstrap the build environment and build redbuild2.
    
```sh
./bootstrap/redbuild.sh
```

this will output `./redbuild.bin` which you can symlink to one of your `$PATH` directories.

Here is a suggested setup:

```sh
mkdir -p ~/.bin
ln -s $(pwd)/redbuild.bin ~/.bin/redbuild
```

Now, you can run `redbuild` from anywhere!

## try the example!

```sh
cd example
redbuild build
```

## detailed usage

### creating the build environment and build script

1. create a `build.docker` file in the project root. this file should contain a `FROM` directive for the base image to use for the build environment. the build environment should contain all the tools necessary to build the project.
it's also very important that the last line of the dockerfile is `CMD ["/bin/bash", "-l"]`. this is necessary for redbuild to work.

    an example `build.docker`:

    ```dockerfile
    FROM debian:bookworm-slim

    # install dependencies
    RUN apt-get update && apt-get install -y \
        bash \
        curl wget xz-utils \
        gcc make libc6-dev libcurl4 \
        git libxml2 \
        && rm -rf /var/lib/apt/lists/* && apt autoremove -y && apt clean


    # install dlang
    RUN curl -fsS https://dlang.org/install.sh | bash -s install ldc-1.30.0 \
        && echo "source ~/dlang/ldc-1.30.0/activate" >> ~/.bashrc

    # set up main to run bash (necessary for redbuild)
    CMD ["/bin/bash", "-l"]
    ```

2. create a `build.sh` file in the project root. this file should contain the steps necessary to build the project. the build script should be written to be run in the build environment.

    `build.sh`:

    ```sh
    #!/bin/bash
    dub build --compiler ldc2 -B release
    ```

that's it! now you can build the project with `redbuild build`, copy it into the project root, and run it. you can also open an interactive shell in the build environment with `redbuild shell`.