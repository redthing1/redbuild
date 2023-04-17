DEFAULT_BUILDENV_DOCKERFILE = """
FROM debian:bookworm-slim

# install dependencies
# NOTE: add any additional dependencies here
RUN apt-get update && apt-get install -y \\
  bash \\
  && rm -rf /var/lib/apt/lists/* && apt autoremove -y && apt clean

# NOTE: add any additional setup steps here

CMD ["/bin/bash", "-l"] # run bash (required by redbuild)
""".strip()
