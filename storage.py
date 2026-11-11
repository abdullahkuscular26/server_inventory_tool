import json
import os
from pathlib import Path

DEFAULT_FILENAME = "servers.json"


def get_data_filename():
    """Finds the file name from environment or uses servers.json."""

    return os.environ.get("INVENTORY_DATA_FILE", DEFAULT_FILENAME)


def load_servers(filename=None):
    """Reads servers from servers.json. If file is missing, returns an empty list."""

    if filename is None:
        filename = get_data_filename()

    file_path = Path(filename)


    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_servers(servers, filename=None):
    """Saves servers to servers.json."""

    if filename is None:
        filename = get_data_filename()

    file_path = Path(filename)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(servers, file, indent=2, ensure_ascii=False)



