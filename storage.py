
import json
import os
from pathlib import Path
import csv
from datetime import datetime

DEFAULT_FILENAME = "servers.json"


def get_data_filename():
    """Finds the file name from environment or uses servers.json."""
    return os.environ.get("INVENTORY_DATA_FILE", DEFAULT_FILENAME)


def load_servers(filename=None):
    """Reads servers from JSON file. If file is missing, returns an empty list."""
    if filename is None:
        filename = get_data_filename()

    file_path = Path(filename)

    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_servers(servers, filename=None):
    """Saves servers to JSON file."""
    if filename is None:
        filename = get_data_filename()

    file_path = Path(filename)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(servers, file, indent=2, ensure_ascii=False)


def export_to_csv(servers, folder_name="reports"):
    """
    Exports the server list to a CSV file with a timestamp in the reports folder.
    Creates the folder automatically if it does not exist.
    Uses second precision to prevent overwriting files in the same minute.
    """
    if not servers:
        return None

    # Create the reports folder if needed.
    reports_dir = Path(folder_name)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Create filename with data and time
    # Add seconds to avoid overwriting files created in the same minute
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    file_path = reports_dir / f"inventory_{timestamp}.csv"

    # Use dictionary keys as CSV headers
    fieldnames = list(servers[0].keys())

    with open(file_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for server in servers:
            writer.writerow(server)

    return str(file_path)