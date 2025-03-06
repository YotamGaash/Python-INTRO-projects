##############################################################################
# FILE: word_dict.py
# EXERCISE: Intro2cs ex6 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash
# DESCRIPTION: this file contains the functions used to create a word mapping dictionary
#              and now is being used by moogles.
# STUDENTS I DISCUSSED THE EXERCISE WITH: Larry Page
# WEB PAGES I USED: The harry Potter wiki.
# NOTES: ...
##############################################################################

""" ~~~~~~~~~~~~~~~~~~~~~~~ imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

import bs4
from typing import List, Dict
import crawl

"""~~~~~~~~~~~~~~~~~~~~~ Constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

DOUBLE_DICT_TYPE = Dict[str, Dict[str, int]]

"""~~~~~~~~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def html_to_word(url_address: str, base_url: str) -> List[str]:
    """
    this function transform a html file to a list of words
    :param url_address: the relative url of the webpage
    :param base_url: the base url of the site
    :return: a list of words found inside the paragraphs in the html file
    """

    txt_list = ""
    html_file = crawl.html_to_txt(url_address, base_url)
    soup = bs4.BeautifulSoup(html_file, 'html.parser')
    for p in soup.find_all(("p")):
        content = p.text
        txt_list += content
    word_list = (txt_list.strip('\n')).strip('\t').split()
    return word_list


def create_word_dict(index_file: str, base_url: str) -> DOUBLE_DICT_TYPE:
    """
    this function creates a string of all the words in an html paragraph
    :param index_file:
    :param base_url:
    :return: a dictionary of words, containing a sub dictionaries for each word for the number of times it appears in a url page.
    """
    word_dict = dict()
    url_list = crawl.get_urls_from_index(index_file)

    for url in url_list:
        word_list = html_to_word(url, base_url)
        for word in word_list:
            if word not in word_dict:
                word_dict[word] = {url: 1}
            else:
                if url in word_dict[word]:
                    word_dict[word][url] += 1
                else:
                    word_dict[word][url] = 1
    return word_dict


if __name__ == '__main__':
    pass
