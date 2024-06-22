"""
Extracts rare words from the source

Note that the website is poorly formatted, each table row (tr and td) are not closed until the very end of the table
which is why we have to resort to string manipulation to extract the data. This is not ideal but it works for now.
"""
import time

import requests
from bs4 import BeautifulSoup

from support.support import Dictionary, extract, SLEEP

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SOURCE = "https://phrontistery.info/"
PAGES = "abcdefghijklmnopqrstuvwxyz"


def extract_page(page: str) -> Dictionary:
    """
    Extract data from a single page
    :param source: the source to extract data from
    :param page: the page to extract data from
    :return: A dictionary of key value pairs for that page
    """
    logger.info(f"Extracting page {page}...")
    time.sleep(SLEEP)
    url = f"{SOURCE}/{page}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = str(soup.find("table", {"class": "words"}))
    if not table:
        logger.warning(f"No table found on page {page}")
        return {}
    data = {}
    rows = table.split("<tr>")
    for row in rows[2:]:
        word, definition = [
            BeautifulSoup(cell, "html.parser").text.strip()
            for cell in row.split("<td>")
            if cell != ""
        ]
        if word != "Word" and definition != "Definition" and word.isascii() and definition.isascii():
            data[word] = definition
    return data


if __name__ == "__main__":
    extract(extract_page, PAGES, "rare_words")

