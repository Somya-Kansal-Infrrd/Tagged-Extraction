"""Services for loading JSON data."""

import json
from typing import Any


def load_json_file(file_name: str) -> Any:
    """Load and return JSON data from a file."""

    with open(
        file_name,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)