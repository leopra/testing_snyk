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

import s3fs
import torch
from outsystems.ai.logs.utils import logtime
from pathvalidate import sanitize_filepath
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel

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
        if os.path.abspath(env_path):
            raise ValueError
        sanitized_path = sanitize_filepath(env_path.replace("..", ""))
        #base_path = "/AAAAA/"
        sanitized_path = os.path.realpath(sanitized_path)

        # common_base = os.path.commonpath([base_path, safe_path]) 
        # if common_base != base_path:
        #     raise ValueError
        # if os.path.basename(safe_path) != env_path:
        #     raise ValueError
        
        return _load2(Path(sanitized_path))

    else:
        return None
    # try:
    #     return _load2()
    # except FileNotFoundError:
    #     pass
    # # If the files don't exist locally, download and unpack them.
    # return _load2()
# = LOCAL_DIR / EXPERIMENT_NAME

def _load2(path: Path) -> Assets:
        with open(f"{path.as_posix()}/metadata.json", "r") as f:
            json_metadata = json.load(f)

        return Assets(
            name=path.stem,
            metadata=metadata,
            metadata=json_metadata,
        )

    