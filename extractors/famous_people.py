"""
Extract famous people from the source
"""

import logging
import time

import requests
from bs4 import BeautifulSoup

from support.support import Dictionary, extract, SLEEP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SOURCE = "https://www.nndb.com/lists/493/000063304/"


def extract_links() -> list[str]:
    """
    Extract links from the source
    :return: List of URLs
    """
    logger.info("Extracting links...")
    response = requests.get(SOURCE)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", {"class": "newslink"})
    return [link["href"] for link in links]


def extract_page(page: str) -> Dictionary:
    """
    Extract data from a single page
    :param page: URL
    :return: Dictionary for that page
    """
    logger.info(f"Extracting page {page}...")
    time.sleep(SLEEP)
    response = requests.get(page)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"border": "0", "cellpadding": "5", "cellspacing": "0"})
    rows = table.find_all("tr")
    data = {}
    for row in rows:
        person, _, claim_to_fame, _, _ = [e.text for e in row.find_all("td")]
        if person.isascii() and claim_to_fame.isascii():
            data[person] = claim_to_fame
    return data


if __name__ == "__main__":
    extract(extract_page, extract_links(), "famous_people")
