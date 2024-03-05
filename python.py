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


def _load2(path: Path = LOCAL_DIR / EXPERIMENT_NAME) -> Assets:
    # sanitize filepath
    if not path.is_absolute():
        sanitized_path = sanitize_filepath(path.as_posix().replace("..", ""))
        if not os.path.isfile(sanitized_path):
            raise ValueError
        sanitized_path = os.path.realpath(sanitized_path)

        with open(f"{sanitized_path}/metadata.json", "r") as f:
            json_metadata = json.load(f)

        return Assets(
            name=path.stem,
            metadata=json_metadata,
        )
    else:
        raise ValueError("Path should not be absolute.")

    