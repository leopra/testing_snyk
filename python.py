"""Download, load and cache pipeline assets."""

import json
import logging
import os
import re
import shutil
import tarfile
from functools import cache
from pathlib import Path
from tarfile import TarFile, TarInfo
from typing import Any, Iterator, TypedDict

from pathvalidate import sanitize_filepath

class Assets(TypedDict):
    """Service assets."""

    name: str
    metadata: dict[str, Any]


@cache
def load_assets() -> Assets:
    """Load the experiment assets corresponding to the defined constants."""
    # in odc, the model is downloaded by platform to this env var location
    env_path = os.environ.get("EXPERIMENT_FOLDER")

    if env_path is not None:
        return _load2(env_path)

    else:
        return None

def _load2(path: Path) -> Assets:
        LOCAL_DIR = Path("aaaaaa")
        REMOTE_DIR = Path("aaaaaa")
        path = path.resolve()
        assert path.is_relative_to(LOCAL_DIR) or path.is_relative_to(APP_DIR)
        # if os.path.abspath(path):
        #     raise ValueError
        # sanitized_path = sanitize_filepath(path.as_posix().replace("..", ""))
        # #base_path = "/AAAAA/"
        # sanitized_path = os.path.realpath(sanitized_path)

        # common_base = os.path.commonpath([base_path, safe_path]) 
        # if common_base != base_path:
        #     raise ValueError
        # if os.path.basename(safe_path) != env_path:
        #     raise ValueError

        with open(sanitized_path/ "metadata.json", "r") as f:
            json_metadata = json.load(f)

        return Assets(
            name=path.stem,
            metadata=json_metadata,
        )

    