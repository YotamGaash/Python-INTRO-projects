##############################################################################
# FILE: search.py
# EXERCISE: Intro2cs ex6 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash
# DESCRIPTION:this file contains the functions used to implement the search engine
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: The harry Potter wiki.
# NOTES: ...
##############################################################################

""" ~~~~~~~~~~~~~~~~~~~~~~~ imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

from typing import Dict, List

"""~~~~~~~~~~~~~~~~~~~~~ Constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

DOUBLE_DICT_TYPE = Dict[str, Dict[str, int]]

"""~~~~~~~~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def get_word_list(words: str, word_dict: DOUBLE_DICT_TYPE) -> List[str]:
    """
    transforming a string of words to a list containing only words from the words dict
    :param word_dict: a dictionary of words
    :param words: a string of query words
    :return: a list of words from the string which appears in the word dictionary
    """

    word_list = []
    split_words = words.split(" ")

    for word in split_words:
        if word_dict.__contains__(word):
            word_list.append(word)
    return word_list


def all_words_in_site(url: str, words: str, word_dict: DOUBLE_DICT_TYPE) -> bool:
    """
    this function checks if all the search query words appear in a page
    :param url: the relative url of a page
    :param words: the words from the search query
    :param word_dict: dictionary of words and urls
    :return:
    """

    word_list = get_word_list(words, word_dict)
    for word in word_list:
        if url not in word_dict[word]:
            return False
    return True


def get_word_val(url: str, words: str, word_dict: DOUBLE_DICT_TYPE) -> int:
    """
    this function returns the minimum number of times of the appearances of one of the words in a page
    :param url: the relative url of a page
    :param words: the words from the search query
    :param word_dict: dictionary of words and urls
    :return:
    """
    word_list = get_word_list(words, word_dict)
    word_vals = []
    for word in word_list:
        word_vals.append(word_dict[word][url])
    if word_vals:
        return min(word_vals)
    else:
        return 0


def valid_pages_list(word_dict: DOUBLE_DICT_TYPE, ranking_dict: Dict[str, int],
                     words: str) -> List[str]:
    """
    this function return all the pages that contains all the words from the search query
    :param ranking_dict: a dictionary of urls and their ranks
    :param words: the words from the search query
    :param word_dict: dictionary of words and urls
    :return: a list of pages that contains all the words
    """
    pages_list = []

    for url in ranking_dict:
        if all_words_in_site(url, words, word_dict):
            pages_list.append(url)
    return pages_list


def result_rank_dict(words: str, word_dict: DOUBLE_DICT_TYPE,
                     rank_dict: Dict[str, int], max_results: int) -> List[str]:
    """
    this function creates a sorted dictionary of pages and their result-ranks with a maximum of "max_results"
            keys
    :param words: the words from the search query
    :param word_dict: dictionary of words and urls
    :param rank_dict: a dictionary of urls and their ranks
    :param max_results: the maximum number of results values to be returned
    :return: a sorted list of result with a maximum of "max_results" values
    """

    pages_list = valid_pages_list(word_dict, rank_dict, words)
    results_val_dict = dict()

    for page in pages_list:
        word_val = get_word_val(page, words, word_dict)
        if word_val > 0:  # adding only pages that contains the words
            results_val_dict[page] = rank_dict[page] * word_val
    # using a line of code from stackoverflow which sorts a dictionary by the values of it's keys
    return (sorted(results_val_dict.items(), key=lambda x: x[1], reverse=True))[:max_results]


def results_to_txt(words: str, word_dict: DOUBLE_DICT_TYPE, rank_dict: Dict[str, int], max_results: int) -> str:
    """

    :param words: the words from the search query
    :param word_dict: dictionary of words and urls
    :param rank_dict: a dictionary of urls and their ranks
    :param max_results: the maximum number of results values to be returned
    :return:a string of the combined results from the result dict
    """
    results_dictionary = result_rank_dict(words, word_dict, rank_dict, max_results)
    results_text = ""
    for result in results_dictionary:
        results_text += f"{result[0]} {result[1]}\n"
    return results_text[:-1]  # removing the last '\n'


