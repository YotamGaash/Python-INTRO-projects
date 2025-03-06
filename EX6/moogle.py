##############################################################################
# FILE: moogle.py
# EXERCISE: Intro2cs ex6 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash
# DESCRIPTION:The main file for the Moogle - the first ever harry potter based search engine.
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: The harry Potter wiki.
# NOTES: ...
##############################################################################

""" ~~~~~~~~~~~~~~~~~~~~~~~ imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
import pickle
from sys import argv
from typing import Dict
from crawl import create_traffic_dict
from word_dict import create_word_dict
from page_rank import create_ranking_dict
from search import results_to_txt

"""~~~~~~~~~~~~~~~~~~~~~ Constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

DOUBLE_DICT = Dict[str, Dict[str, int]]
READ_BINARY = 'rb'
WRITE_BINARY = 'wb'
CRAWL = "crawl"
RANK = "page_rank"
WORDS = "word_len_dict"
SEARCH = "search"



"""~~~~~~~~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def write_a_pickle(data, out_file):
    """
    this function writes data into a pickle file
    :param data: the data we want to write to a pickle file
    :param out_file: the name and destination of the output file
    :return: None
    """
    with open(out_file, "wb") as f:
        pickle.dump(data, f)


def read_a_pickle(filename):
    """
    this function reads data from a pickle file and assign it to an object
    :param filename: the name/location of the pickle file
    :return: the data from the pickle file
    """
    with open(filename, "rb") as f:
        return pickle.load(f)


def crawl(base_url: str, index_file: str, out_file: str):
    """
    creating a traffic dictionary with the base_url and an index file of urls
    and saving it to a pickle file.
    :param base_url: the url of the main site used as prefix to the urls from the index file
    :param index_file: a txt file containing a list of urls
    :param out_file: a traffic dictionary saved as a pickle file
    :return: None
    """

    traffic_dictionary = create_traffic_dict(index_file, base_url)
    write_a_pickle(traffic_dictionary, out_file)


def page_rank(iterations: int, dict_file: str, out_file: str):
    """
    creating a ranking dictionary with the using a traffic dict and applying the ranking
    algorithm to in for the given number of iterations.
    :param iterations: the number of iteration used for applying the ranking algorithm
    :param dict_file: a pickle file of a traffic dict
    :param out_file: a ranking dict saved as a pickle file
    :return: None
    """
    traffic_dictionary = read_a_pickle(dict_file)
    ranking_dictionary = create_ranking_dict(traffic_dictionary, iterations)
    write_a_pickle(ranking_dictionary, out_file)


def words_dict(base_url: str, index_file: str, out_file: str):
    """
    creating a word dict with the base_url and an index file of urls
    and saving it to a pickle file.
    :param base_url: the url of the main site used as prefix to the urls from the index file
    :param index_file: a txt file containing a list of urls
    :param out_file: a search dictionary saved as a pickle file
    :return: None
    """
    words_dictionary = create_word_dict(index_file, base_url)
    write_a_pickle(words_dictionary, out_file)


def search(query: str, ranking_dict_file: str, words_dict_file: str, max_results: int):
    """
    creating a text file containing the best search results (with a given maximum length)
    for a search query. using the word_len_dict and the ranking dict.
    :param query: the words we wish to search
    :param ranking_dict_file: a location of a pickle file of a ranking dict
    :param words_dict_file: a location of a pickle file of a words dict
    :param max_results: the maximum number of search results to be given
    :return: None
    """

    ranking_dictionary = read_a_pickle(ranking_dict_file)
    words_dictionary = read_a_pickle(words_dict_file)
    results_txt = results_to_txt(query, words_dictionary, ranking_dictionary, max_results)
    print(results_txt)

def create_result_txt():
    base_url = "https://www.cs.huji.ac.il/~intro2cs1/ex6/wiki/"
    index_list = "small_index.txt"
    r = 100
    word_list = ["scar", "Crookshanks", "Horcrux", "Pensieve McGonagall", "broom wand cape"]

    crawl(base_url,index_list,"traffic_dict.pickle")
    page_rank(r,"traffic_dict.pickle", "rank_dict.pickle")
    words_dict(base_url,index_list,"words_dict.pickle")
    for word in word_list:
        search(word,"rank_dict.pickle","words_dict.pickle", 4)
        print('*' * 10)


def main():
    """
    the main function for our Moogle search engine. Based on the args it get from the user
    it performs either the crawl, word_dict, page_rank or search commands.
    :return:
    """
    if argv[1] == CRAWL:
        crawl(argv[2], argv[3], argv[4])
    elif argv[1] == WORDS:
        words_dict(argv[2], argv[3], argv[4])
    elif argv[1] == RANK:
        page_rank(int(argv[2]), argv[3], argv[4])
    elif argv[1] == SEARCH:
        search(argv[2], argv[3], argv[4], int(argv[5]))
    else:
        print("An invalid argument has been entered")
        return
    pass


if __name__ == '__main__':
    main()
