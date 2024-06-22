"""
Extracting film taglines
"""

import logging
import time

import requests
from bs4 import BeautifulSoup

from support.support import Dictionary, extract, SLEEP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SOURCE = "http://www.impawards.com/taglines"
SOURCE_WITH_SEED = f"{SOURCE}/a1.html"


def extract_links() -> list[str]:
    """
    Extract links from the source
    :return: a list of URLs
    """
    logger.info("Extracting links...")

    def parse_current(seed_page: str):
        time.sleep(SLEEP)
        sub_response = requests.get(seed_page)
        sub_soup = BeautifulSoup(sub_response.text, "html.parser")
        divs = sub_soup.find_all("div", {"class": "col-xs-12"})
        continuation_links = [f"{SOURCE}/{l['href']}" for l in divs[4].find("center").find_all("a")]
        return [seed_page] + continuation_links

    response = requests.get(SOURCE_WITH_SEED)
    first_soup = BeautifulSoup(response.text, "html.parser")
    link_buttons = first_soup.find("div", {"class": "btn-group"})
    letter_links = [f"{SOURCE}/{l['href']}" for l in link_buttons.find_all("a") if l.text != "#"]
    return sum([parse_current(ll) for ll in letter_links], [])


def extract_page(page: str) -> Dictionary:
    """
    Extract taglines
    :param page: URL
    :return: A dictionary with taglines
    """
    logger.info(f"Extracting page {page}...")
    time.sleep(SLEEP)
    response = requests.get(page)
    soup = BeautifulSoup(response.text, "html.parser")
    taglines = soup.find_all("div", {"class": "col-xs-12"})[4]
    center_tag = taglines.find("center")
    br_tags = center_tag.find_all_next("br", limit=2)
    last_br_tag = br_tags[-1]
    data = {}
    raw_data = last_br_tag.find_all_next(string=True)
    for i in range(0, len(raw_data), 3):
        if raw_data[i] == '\n':
            break
        tagline = BeautifulSoup(raw_data[i].strip(' -'), "html.parser").text.strip().strip('"')
        title = raw_data[i+1]
        if title.isascii() and tagline.isascii():
            data[title] = tagline
    return data


if __name__ == "__main__":
    extract(extract_page, extract_links(), "film_taglines")
