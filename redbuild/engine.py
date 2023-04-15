import sh
from enum import Enum


class ContainerEngine(Enum):
    podman = "podman"
    docker = "docker"

    def __str__(self):
        return self.value


def detect_container_engine():
    # get container engine
    # we prefer podman to docker, but we'll use docker if podman is not available

    if sh.which("podman"):
        return ContainerEngine.podman
    elif sh.which("docker"):
        return ContainerEngine.docker
    else:
        raise Exception(
            "No usable container engine found. Please install podman or docker."
        )


def get_container_engine_command(container_engine: ContainerEngine):
    return sh.Command(container_engine.value)
