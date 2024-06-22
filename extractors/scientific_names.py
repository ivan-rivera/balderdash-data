"""
Scientific names extractor
"""

import time

import re
import requests
from bs4 import BeautifulSoup

from support.support import Dictionary, extract, SLEEP

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SOURCE = "https://www.esveld.nl/catalen/engnaam.htm"


def extract_page(page: str) -> Dictionary:
    logger.info(f"Extracting page {page}...")
    time.sleep(SLEEP)
    response = requests.get(page)
    soup = BeautifulSoup(response.text, "html.parser")
    data = {}
    for table in soup.find_all("table", { "border":"", "cellpadding": "5", "width": "96%"}):
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) == 2:
                common, latin = [td.text.strip() for td in tds]
                if latin != common and latin.isascii() and common.isascii():
                    data[latin] = common
    return data


if __name__ == "__main__":
    extract(extract_page, [SOURCE], "scientific_names")
