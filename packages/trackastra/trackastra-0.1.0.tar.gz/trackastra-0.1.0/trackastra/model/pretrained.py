import logging
import os
from typing import Optional
import zipfile
from pathlib import Path

import requests
from pydantic import validate_call
from tqdm import tqdm
import tempfile 
import shutil

logger = logging.getLogger(__name__)

_MODELS = {
    "ctc": "https://github.com/weigertlab/trackastra-models/releases/download/v0.1/ctc.zip",
    "general_2d": "https://github.com/weigertlab/trackastra-models/releases/download/v0.1.1/general_2d.zip",
}


def download_and_unzip(url: str, dst: Path):
    # TODO make safe and use tempfile lib
    if dst.exists():
        print(f"{dst} already downloaded, skipping.")
        return
    
    # get the name of the zipfile
    zip_base = Path(url.split("/")[-1])

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        zip_file = tmp / zip_base
        # Download the zip file
        download(url, zip_file)

        # Unzip the file
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(tmp)

        shutil.move(tmp/zip_base.stem, dst)


def download(url: str, fname: Path):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get("content-length", 0))
    with open(str(fname), "wb") as file, tqdm(
        desc=str(fname),
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


@validate_call
def download_pretrained(name: str, download_dir: Optional[Path] = None):
    # TODO make safe, introduce versioning
    if download_dir is None:
        download_dir = Path("~/.trackastra/.models").expanduser()
    else: 
        download_dir = Path(download_dir)

    download_dir.mkdir(exist_ok=True, parents=True)
    try:
        url = _MODELS[name]
    except KeyError:
        raise ValueError(
            f"Pretrained model `name` is not available. Choose from {list(_MODELS.keys())}"
        )
    folder = download_dir / name
    download_and_unzip(url=url, dst=folder)
    return folder
