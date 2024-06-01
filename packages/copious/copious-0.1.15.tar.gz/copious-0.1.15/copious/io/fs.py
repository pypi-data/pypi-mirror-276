from pathlib import Path
import functools
import tempfile
import json
import yaml
from typing import List, Dict, Union


def read_json(path: Path) -> Union[Dict, List[Dict]]:
    with open(path) as f:
        j = json.load(f)
    return j


def write_json(json_data: Union[Dict, List[Dict]], path: Path, prettify: bool = True) -> None:
    with open(path, "w") as f:
        if prettify:
            json.dump(json_data, f, indent=4)
        else:
            json.dump(json_data, f)


def read_yaml(path: Union[str, Path]) -> Union[Dict, List[Dict]]:
    with open(path) as f:
        y = yaml.safe_load(f)
    return y


def write_yaml(data: Union[Dict, List[Dict]], path: Path) -> None:
    with open(path, "w") as f:
        yaml.dump(data, f)


def create_empty_temp_file(prefix=None, suffix=None) -> Path:
    _, path = tempfile.mkstemp(prefix=prefix, suffix=suffix, text=True)
    return Path(path)


def mktmpdir():
    tmp_dir = Path(tempfile.mktemp())
    tmp_dir.mkdir()
    return tmp_dir


def create_test_files(root_dir, files):
    root_dir = Path(root_dir)
    _paths = [root_dir / f for f in files]
    for p in _paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()


def ensured_path(input, ensure_parent=False):
    """Often used in the scenario that the path we want to write things to is ensured to be exist."""
    p = Path(input)
    if ensure_parent:
        p.parent.mkdir(parents=True, exist_ok=True)
    else:
        p.mkdir(parents=True, exist_ok=True)
    return p


parent_ensured_path = functools.partial(ensured_path, ensure_parent=True)

__all__ = [
    "read_json",
    "write_json",
    "create_empty_temp_file",
    "mktmpdir",
    "create_test_files",
    "ensured_path",
    "parent_ensured_path",
]
