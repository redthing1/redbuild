from typing import List, Optional
from dataclasses import dataclass

# DEFAULT_BUILDENV_DOCKERFILE = """
# FROM debian:bookworm-slim

# # install dependencies
# # NOTE: add any additional dependencies here
# RUN apt-get update && apt-get install -y \\
#   bash \\
#   && rm -rf /var/lib/apt/lists/* && apt autoremove -y && apt clean

# # NOTE: add any additional setup steps here

# CMD ["/bin/bash", "-l"] # run bash (required by redbuild)
# """.strip()

BUILDENV_DOCKERFILE_TEMPLATE = """
FROM {base_image}

# install dependencies
# NOTE: add any additional dependencies here
RUN apt-get update && apt-get install -y \\
    bash \\
    {additional_packages} \\
    && rm -rf /var/lib/apt/lists/* && apt autoremove -y && apt clean

# NOTE: add any additional setup steps here
{additional_setup}

CMD ["/bin/bash", "-l"] # run bash (required by redbuild)
""".strip()


@dataclass
class BuildEnv:
    base_image: str
    additional_packages: List[str]
    additional_setup: List[str]


def compose_dockerfile(build_env: BuildEnv) -> str:
    # create the dockerfile contents from the template

    return BUILDENV_DOCKERFILE_TEMPLATE.format(
        base_image=build_env.base_image,
        additional_packages=" ".join(build_env.additional_packages),
        additional_setup="\n".join(build_env.additional_setup),
    )

DEFAULT_BUILDENV = BuildEnv(
    base_image="debian:bookworm-slim",
    additional_packages=[],
    additional_setup=[],
)
