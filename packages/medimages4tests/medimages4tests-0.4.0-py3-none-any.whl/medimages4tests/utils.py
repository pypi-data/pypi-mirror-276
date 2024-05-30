from tempfile import mkdtemp
import requests
import tarfile
import shutil
import os
import typing as ty
from pathlib import Path
import openneuro
import attrs
from . import base_cache_dir


@attrs.define
class OpenneuroSpec:
    dataset: str
    tag: str
    path: Path = attrs.field(converter=Path)


def retrieve_from_openneuro(
    sample, cache_path, suffixes=(".nii.gz", ".json"), force_download=False
):
    """Retrieves an image from the OpenNeuro repository"""
    if not cache_path.parent.exists():
        cache_path.parent.mkdir(parents=True)
    out_path = cache_path.with_suffix(suffixes[0])
    if not out_path.exists() or force_download:
        tmpdir = Path(mkdtemp())
        openneuro.download(
            dataset=sample.dataset,
            tag=sample.tag,
            target_dir=str(tmpdir),
            include=[str(sample.path)],
        )
        for ext in suffixes:
            shutil.copyfile(
                (tmpdir / sample.path).with_suffix(ext), cache_path.with_suffix(ext)
            )
    return out_path


def retrieve_from_github(
    org: str,
    repo: str,
    path: str,
    tag: str = "main",
    compressed: bool = True,
    cache_dir: ty.Union[Path, str, None] = None,
) -> Path:
    """Retrieves a sample file from a path within a GitHub repository

    Parameters
    ----------
    org: str
        the Github organisation
    repo : str
        the name of the git repository within the Github organisation
    path : str
        the path to the file relative to the repository
    tag : str, optional
        the git tag (version) to use, "main" by default
    compressed : bool, optional
        whether the file within the git repo has been archived with tar/gzip and
        needs to be uncompressed before use, True by default
    cache_dir : Path | str, optional
        the directory in which to download and cache the requested file, by default uses
        "~/.medimages/cache/github"
    """
    if cache_dir is None:
        cache_dir = base_cache_dir / "github"
    else:
        cache_dir = Path(cache_dir).expanduser()
    cache_path = (cache_dir / repo / tag).joinpath(*path.split("/"))
    if cache_path.exists():
        return cache_path
    if not cache_path.parent.exists():
        cache_path.parent.mkdir(parents=True)
    url = f"https://raw.githubusercontent.com/{repo}/{tag}/{path}"
    if compressed:
        url += ".tar.gz"
    response = requests.get(url)
    if response.status_code != "200":
        raise ValueError(f"Did not find a file to download at '{url}'")
    if compressed:
        tmp_dir = Path(mkdtemp())
        download_path = tmp_dir / url.split("/")[-1]
    else:
        download_path = cache_path
    with open(download_path, "wb") as f:
        f.write(response.content)
    if compressed:
        extract_dir = tmp_dir / "extracted"
        extract_dir.mkdir()
        with tarfile.open(download_path) as tfile:
            tfile.extractall(path=extract_dir)
        dir_contents = list(extract_dir.iterdir())
        if len(dir_contents) > 1:
            raise ValueError(
                f"Contents or tar file at {url} contain more than one file/sub-dir ({dir_contents})"
            )
        os.rename(dir_contents[0], cache_path)
    return cache_path
