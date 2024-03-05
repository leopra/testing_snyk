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

from data_elements.torch_model import DATA_TYPE, TORCH_COMPILE, ModelArgs, Transformer
from data_elements.torch_pipeline import TextGenerationPipeline, generate


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
        return _load2(Path(env_path))

    try:
        return _load2()
    except FileNotFoundError:
        pass
    # If the files don't exist locally, download and unpack them.
    return _load2()

def _load(path: Path = LOCAL_DIR / EXPERIMENT_NAME) -> Assets:
    metadata_path = path / "metadata.json"
    metadata_path = sanitize_filepath(metadata_path.as_posix().replace("..", ""))

    # #tokenizer = AutoTokenizer.from_pretrained(path / "tokenizer")
    # base_path = "/AAAAA/"
    # if not os.path.isfile(metadata_path):
    #    raise ValueError
    safe_path = os.path.realpath(metadata_path)

    # common_base = os.path.commonpath([base_path, safe_path]) 
    # if common_base != base_path:
    #     raise ValueError
    
    if os.path.basename(safe_path) != metadata_path:
        # Invalid - path traversal detected
        raise ValueError

    #metadata_path = os.path.join(path,"metadata.json")
    #safe_path = metadata_path
    with open(safe_path, "r") as f:
        metadatad=json.load(f)
    return Assets(
        name=path.stem,
        metadata=metadatad,
    )
    # sanitize filepath
    # if not os.path.isabs(path):
    #     path = Path(sanitize_filepath(path.as_posix().replace("..", "")))
    #     metadata_path = os.path.join(path,"metadata.json")
    #     metadata_path = path / "metadata.json"
    
    #metadata_path = Path(os.path.join(path,"metadata.json"))

    metadatad = json.loads(metadata_path.read_text())
    return Assets(
        name=path.stem,
        metadata=metadatad,
    )
    # else:
    #     raise ValueException 


def _load2(path: Path = LOCAL_DIR / EXPERIMENT_NAME) -> Assets:
    # sanitize filepath
    if not path.is_absolute():
        sanitized_path = sanitize_filepath(path.as_posix().replace("..", ""))
        with open(f"{sanitized_path}/metadata.json", "r") as f:
        json_metadata = json.load(f)

        return Assets(
            name=path.stem,
            metadata=metadata,
            metadata=json_metadata,
        )
    else:
        raise ValueError("Path should not be absolute.")

    