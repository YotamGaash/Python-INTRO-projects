##############################################################################
# FILE: ex12_utils.py
# EXERCISE: Intro2cs ex12 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash, Samuel Hayat [REDACTED] 
# DESCRIPTION: this is a utility file for the game logic
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
##############################################################################


from boggle_board import Board
from typing import List, Tuple, Any, Optional

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Helper functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def is_board_really_a_board(board: Any) -> Board:
	"""
    if the board is not a Board object, it will be returned as a board object.
    :param board: a board that might not be a board object
    :return: Board object
    """
	if not isinstance(board, Board):
		return Board(board)
	return board


def get_word_at_path(board: Board, path: List[Tuple[int, int]]) -> str:
	"""
    creates a string from all the letters in the cords in the path
    :param board: a Board object
    :param path: a list of cords from the board
    :return: the word created by all the letters in the cords
    """
	return "".join([board.get_letter_at_cord(cord) for cord in path])


def find_word_path(board: Board, word: str) -> List[List[Tuple[int, int]]]:
	"""
    search if there is a sliced_word path on the board for a certain sliced_word
    :param board: board object
    :param word: a string
    :return: a list of the cords of the path if there is a path. None otherwise.
    """

	def _find_word_path_helper(board: Board, sliced_word: str, current_path: List[Tuple[int, int]],
	                           all_paths: List[List[Tuple[int, int]]]) -> List[List[Tuple[int, int]]]:
		""" helper function for the find sliced_word path recursion"""
		if len(sliced_word) == 0:
			all_paths.append(current_path)
			return

		if len(sliced_word) < 0:
			return

		for neighbor in board.get_neighbors(current_path[-1]):
			if '\n' + board.get_letter_at_cord(neighbor) in '\n' + sliced_word and neighbor not in current_path:
				_find_word_path_helper(board, sliced_word[len(board.get_letter_at_cord(neighbor)):],
				                       current_path + [neighbor], all_paths)
		return all_paths

	all_word_paths = []
	for row in range(board.board_height):
		for col in range(board.board_width):
			if '\n' + board.get_letter_at_cord((row, col), ) in '\n' + word:
				word_paths = _find_word_path_helper(board, word[len(board.get_letter_at_cord((row, col), )):],
				                                    [(row, col)], [])
				if word_paths:
					all_word_paths += word_paths

	return all_word_paths


def all_word_paths_dictionary(board: Board, words: Any):
	"""
    Creates a dictionary of all the possible word paths in a board. the keys of the dictionary are words
    and the value are a list of the valid paths of the word.
    :param board:
    :param words:
    :return:
    """
	all_word_path_dict = dict()
	for word in words:
		word_paths = find_word_path(board, word)
		if word_paths:
			all_word_path_dict[word] = word_paths
	return all_word_path_dict


def find_path_helper(n: int, board: Board, words: Any, current_path: List[Tuple[int, int]],
                     all_valid_paths: List[List[Tuple[int, int]]], all_invalid_paths: List[List[Tuple[int, int]]],
                     all_words_str: str, search_by_word: bool = False) -> Optional[List[List[Tuple[int, int]]]]:
	"""
    A helper function for both the find_length_n_paths and find_length_n_words functions, it finds all the paths
    starting from a certain cord in the board with a length n or all the paths of words with n letters
    if the paths match a word from the word list.

    :param all_valid_paths: all the valid paths found so far
    :param all_words_str: a string of all the words in the word list combined
    :param n: the length of the desired path
    :param board: a Board object
    :param current_path: the current path searched for so far
    :param all_invalid_paths: all the bad paths
    :param search_by_word: default value is False. the value is changed to the len of a letter in a cord
                           in the board if we use the helper function inside find_length_n_words()
    :return: all the valid paths found
    """

	if current_path in all_invalid_paths:  # skipping all the invalid paths that were already found
		return

	if n <= 0:  # stopping condition for the recursion
		if is_valid_path(board, current_path, words):
			all_valid_paths.append(current_path)
		else:
			all_invalid_paths.append(current_path)
		return

	for neighbor in board.get_neighbors(current_path[-1]):
		if "\n" + get_word_at_path(board, current_path + [neighbor]) in all_words_str:

			if search_by_word:  # if we use the function to search by word length
				find_path_helper(n - len(board.get_letter_at_cord(neighbor)), board, words, current_path + [neighbor],
				                 all_valid_paths, all_invalid_paths, all_words_str, True)

			else:  # if we search by path length
				find_path_helper(n - 1, board, words, current_path + [neighbor],
				                 all_valid_paths, all_invalid_paths, all_words_str)

	return all_valid_paths


def path_finder(n: int, board: Board, words: Any, search_by_word=False) -> Optional[List[List[Tuple[int, int]]]]:
	"""
    A helper function for both the find_length_n_paths and find_length_n_words functions, it finds all the paths
    starting from a certain cord in the board with a length n or all the paths of words with n letters
    if the paths match a word from the word list.

    :param n: an int indicating the length of the paths (or words) to be searched
    :param board: a Board object
    :param search_by_word: default value is False. the value is changed to the len of a letter in a cord
                           in the board if we use the helper function inside find_length_n_words()
    :return: all the valid paths found
    """

	board = is_board_really_a_board(board)
	all_valid_paths = []
	all_words_str = "\n" + "\n".join(words)

	for row in range(board.board_height):
		for col in range(board.board_width):

			if search_by_word:  # if we are searching by word length
				if len(board.get_letter_at_cord((row, col))) == n:  # if the letters in a cord contain an entire word
					if board.get_letter_at_cord((row, col)) in words:
						new_paths = [[(row, col), ]]
				else:
					new_paths = find_path_helper(n - len(board.get_letter_at_cord((row, col), )),
					                             board, words, [(row, col)], [], [], all_words_str, True)

			else:  # if we are searching by path length
				new_paths = find_path_helper(n - 1, board, words, [(row, col)], [], [], all_words_str)
			if new_paths:
				all_valid_paths.extend(new_paths)

	return all_valid_paths


"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Utility Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def is_valid_path(board: Board, path: Tuple[Tuple[int, int]], words: Any) -> Optional[str]:
	"""
    this function checks if a path in the board is valid; meaning:
    1. no cord repeats itself twice
    2. all cords are adjacent and inside the board
    3. the word created by all the letters in the path is in the words

    :param board: a Board object
    :param path: a tuple of cords
    :param words: an iterable object containing strings for words
    :return: returns the word in the path if the path is valid. None otherwise
    """

	board = is_board_really_a_board(board)

	if not path:  # empty path
		return None

	# checking if a cord in the path repeats itself twice (or more times).
	if len(set(path)) < len(path):
		return None

	# checking if all the cords in the path are adjacent to each other.
	if not board.valid_cord(path[-1]):
		return None
	for i in range(len(path) - 1):
		if not path[i + 1] in board.get_neighbors(path[i]) or not board.valid_cord(path[i]):
			return None

	path_word = get_word_at_path(board, path)
	if path_word in set(words):  # converting to set for O(1) complexity instead of O(n)
		return path_word

	return None


def find_length_n_paths(n: int, board: Board, words: Any) -> List[List[Tuple[int, int]]]:
	"""
    this function creates a list of all the valid paths with length of n inside the board.

    :param n: desired length for the paths
    :param board: a Board object
    :param words: an iterable object containing strings of words
    :return: a list containing all the valid paths with the length of n
    """
	return path_finder(n, board, words)


def find_length_n_words(n: int, board: Board, words: Any) -> List[List[Tuple[int, int]]]:
	"""
    this function find all the paths in the board of words with n letters from the word list.
    :param n: the length of the words we wish to find
    :param board: a Board object
    :param words: an iterable object containing strings of words
    :return: a list containing all the valid paths of words with the length of n
    """
	return path_finder(n, board, words, True)


def max_score_paths(board: Board, words: Any) -> List[List[Tuple[int, int]]]:
	"""
    this function searches for the paths in the board that will return the max score. the score is calculated
    by the length of the path of a word.
    :param board: a board object
    :param words: an iterable object containing strings of words
    :return: a list containing all the paths that contain the words with the max score
    """
	board = is_board_really_a_board(board)
	all_path_dict = all_word_paths_dictionary(board, words)
	return [max(all_path_dict[word], key=len) for word in all_path_dict]  # list of the longest paths for each word


if __name__ == '__main__':
	pass
