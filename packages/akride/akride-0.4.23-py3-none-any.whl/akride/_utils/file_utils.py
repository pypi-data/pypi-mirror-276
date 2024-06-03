import json
import os.path
import shutil
import tempfile
from pathlib import Path
from typing import Any, List, Optional

from pyakri_de_utils.file_utils import create_directory

from akride.core._filters.enums import FilterTypes


def copy_files_to_dir(files: List[str], dst_dir: str):
    for file in files:
        # file[1:] -> to get the file path without "/"
        dest_file_path = Path(dst_dir, *Path(file).parts[1:])

        create_directory(str(dest_file_path.parent))
        shutil.copy(file, dest_file_path)


def get_file_name_from_path(filepath: str) -> str:
    return Path(filepath).name


def create_temp_directory(dir_path: str):
    return tempfile.TemporaryDirectory(dir=dir_path)


def remove_directory(directory: str):
    if os.path.exists(directory):
        shutil.rmtree(directory)


def concat_file_paths(*file_path_list) -> str:
    return str(Path(*file_path_list))


def get_filter_output_dir(
    par_dir: str,
    filter_type: FilterTypes,
    token_number: Optional[int] = None,
) -> str:
    output_dir = concat_file_paths(par_dir, filter_type.value, "outputs")
    if token_number is not None:
        output_dir = concat_file_paths(output_dir, str(token_number), "o1")
    return output_dir


def get_sorted_dirs_from_path(path: str):
    def get_creation_time(item):
        item_path = concat_file_paths(path, item)
        return os.path.getctime(item_path)

    items = os.listdir(path)
    sorted_items = sorted(items, key=get_creation_time)
    return sorted_items


def get_json_from_file(file: str, obj_hook: Optional[Any] = None) -> Any:
    with open(file, "rb") as f:
        return json.load(f, object_hook=obj_hook)
