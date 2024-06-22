import json
from typing import Callable
from functools import reduce
from pathlib import Path

SLEEP = 0.1  # seconds to sleep in between requests

Dictionary = dict[str, str]


def to_json(data: Dictionary, filename: str) -> None:
    """
    Save data to a json file
    :param data: a dictionary of key value pairs (strings)
    :param filename: name of the file to save it in
    :return: None
    """
    folder = "../data"
    Path(folder).mkdir(parents=True, exist_ok=True)
    with open(f"{folder}/{filename}.json", "w") as f:
        json.dump(data, f, indent=4)


def extract(page_extractor: Callable[[str], Dictionary], pages: list[str] | str, filename: str) -> None:
    """
    Extract data from the source
    :return: a dictionary of key value pairs (strings)
    """
    data = reduce(lambda x, y: {**x, **y}, [page_extractor(page) for page in pages])
    to_json(data, filename)
