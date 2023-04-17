import os
import sys
import random
import hashlib

# CWD_DIRNAME=$(basename "$CWD")
# # lowercase and alphanumeric only
# CWD_DIRNAME=$(echo "$CWD_DIRNAME" | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]')
# CWD_HASH=$(echo "$CWD" | sha256sum | head -c 8)

# # BUILDER_TAG=builder_$(head /dev/urandom | tr -dc a-z0-9 | head -c10)
# BUILDER_TAG=builder_${CWD_DIRNAME}_${CWD_HASH}


def get_builder_image_name(cwd):
    # expand cwd to absolute path
    cwd = os.path.abspath(cwd)
    cwd_dirname = os.path.basename(cwd).lower()
    cwd_dirname = "".join([c for c in cwd_dirname if c.isalnum()])

    cwd_hash = hashlib.sha256(cwd.encode("utf-8")).hexdigest()[:8]

    builder_tag = f"redbuild_builder_{cwd_dirname}_{cwd_hash}"

    return builder_tag


def parse_secondary_args(args):
    return [arg for arg in args.split(" ") if arg]
