##############################################################################
# FILE: page_rank.py
# EXERCISE: Intro2cs ex6 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash
# DESCRIPTION: this file contains the implementation of the page rank algorithm originally used by google
#              and now is being used by moogles.
# STUDENTS I DISCUSSED THE EXERCISE WITH: Larry Page
# WEB PAGES I USED: The harry Potter wiki.
# NOTES: ...
##############################################################################


""" ~~~~~~~~~~~~~~~~~~~~~~~ imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

from typing import Dict, Union
from copy import deepcopy

"""~~~~~~~~~~~~~~~~~~~~~~ Constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

PARAGRAPH = 'p'
HTML_LINK = 'a'
HREF_ATTR = 'href'
DOUBLE_DICT_TYPE = Dict[str, Dict[str, int]]

"""~~~~~~~~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def sum_of_links(page_dictionary: Dict[str, Union[int, float]]) -> Union[int, float]:
    """
    this function returns the total number of links in a given page
    dictionary
    :param page_dictionary: dictionary of the number of time each link is appears
    in a given page
    :return: the sum of the links the page
    """

    link_sum = 0

    for link in page_dictionary:
        link_sum += page_dictionary[link]
    return link_sum


def create_sum_dict(traffic_dict: DOUBLE_DICT_TYPE):
    """
    this function creates dictionary with the total sum of links in each page
    :param traffic_dict:
    :return: sum_dict - the dictionary with the sum of links for each page
    """
    sum_dict = dict()
    for page_dict in traffic_dict:
        sum_dict[page_dict] = sum_of_links(traffic_dict[page_dict])
    return sum_dict


def create_ranking_dict(original_dict: DOUBLE_DICT_TYPE, r: int) -> Dict[str, float]:
    """
    this function creates a ranking dictionary which assign each page it's rank based on the number of
    times it was referenced by other pages. the function runs the applies
    :param original_dict: the dictionary of all the links between pages in a list of webpages
    :param r: the number of iterations for which the function "runs"
    :return: a dictionary of the webpages and their ranks.
    """

    traffic_dictionary = deepcopy(original_dict)
    rank_dictionary = {page: 1 for page in traffic_dictionary}  # setting the rank of all the pages to one
    sum_dictionary = create_sum_dict(traffic_dictionary)

    for iteration in range(r):
        new_rank_dictionary = {page: 0 for page in traffic_dictionary}
        for page in rank_dictionary:
            page_link_sum = sum_of_links(traffic_dictionary[page])
            for link in traffic_dictionary[page]:
                new_rank_dictionary[link] += rank_dictionary[page] * \
                                             (traffic_dictionary[page][link] / page_link_sum)
        rank_dictionary = deepcopy(new_rank_dictionary)
    return rank_dictionary

