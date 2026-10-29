import json
from pathlib import Path

def load_json_data(file_name: str):
    """
    Load JSON data from a file.

    Args:
        file_name (str): The name of the JSON file to load.
    """
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "data" / file_name

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)