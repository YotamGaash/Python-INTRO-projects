##############################################################################
# FILE: crawl.py
# EXERCISE: Intro2cs ex6 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash
# DESCRIPTION: this file contains all the functions used to create a traffic dictionary
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: The harry Potter wiki.
# NOTES: ...
##############################################################################

""" ~~~~~~~~~~~~~~~~~~~~~~~ imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

import bs4
import requests
from typing import List, Dict
from urllib import parse


"""~~~~~~~~~~~~~~~~~~~~~~ Constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


PARAGRAPH = 'p'
HTML_LINK = 'a'
HREF_ATTR = 'href'
DOUBLE_DICT_TYPE = Dict[str, Dict[str, int]]

"""~~~~~~~~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

def get_urls_from_index(index_file_path: str) -> List[str]:
    """
    this function reads the relative urls from an index file and return a list of the full url links
    :param index_file_path: the path to the index_file
    :return: a list of urls
    """

    index_list = []
    with open(index_file_path) as index_file:
        for line in index_file.readlines():
            index_list.append(line.strip("\n"))
        index_file.close()
    return index_list


def html_to_txt(url_path: str, base_url: str) -> str:
    """
    this function gets an html file as text from a url site
    :param base_url: the url for the main site
    :param url_path: the relative path of the url
    :return: the text of the html file of the site.
    """

    full_url = parse.urljoin(base_url, url_path)
    response = requests.get(full_url)
    return response.text

def create_link_dict(html_file: str, index_list: List[str]) -> Dict[str, int]:
    """
    this function creates a dictionary for the number of time each link is referenced inside a given site
    :param html_file: the html file of the given site
    :param index_list: a list of urls
    :return: a dictionary of a url and its connections to other urls
    """

    link_dict = dict()
    soup = bs4.BeautifulSoup(html_file, 'html.parser')

    for p in soup.find_all(PARAGRAPH):
        for link in p.find_all("a"):
            target_link = link.get("href")
            if target_link in index_list:
                if target_link in link_dict:
                    link_dict[target_link] += 1
                else:
                    link_dict[target_link] = 1
    return link_dict


def create_traffic_dict(index_file: str, base_url: str) -> DOUBLE_DICT_TYPE:
    """
    this function creates a dictionary of link_dictionaries for each link in the index list"
    :param index_file: a file containing list of urls
    :param base_url: the url of the main site
    :return: a dictionary of all the urls and their connections to other sites
    """

    traffic_dictionary = dict()
    link_list = get_urls_from_index(index_file)

    for link in link_list:
        traffic_dictionary[link] = create_link_dict(html_to_txt(link,base_url),link_list)

    return traffic_dictionary



