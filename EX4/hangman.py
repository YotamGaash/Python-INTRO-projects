__Author__ = "Yotam Gaash"
__email__ = "Yotam.Gaosh@mail.huji.ac.il"

#################################################################
# FILE : hangman2.py
# WRITER : Yotam Gaash , Gaash , [REDACTED]
# EXERCISE : intro2cs1 ex4 2021
# DESCRIPTION: This program is a hangman game without the actual hanged person
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: stack overflow
# NOTES: ...
#################################################################

import hangman_helper  # importing functions from hangman helper

""" magic numbers """

POINTS_INITIAL = 10
HINT_LENGTH = 3

LETTER = 1
WORD = 2
HINT = 3

ABC = 'abcdefghijklmnopqrstuvwxyz'

# messages
STARTING_MSG = 'Good luck! try not to choke.'
DEFAULT_MSG = 'Hang in there'
INVALID_INPUT = "ERROR: the input entered is not a valid char"
INVALID_LETTER = "ERROR: please enter a smaller case ABC letter"
SAME_LETTER_AGAIN = "ERROR: this letter was already used before"
NO_HINTS = "ERROR: no hints! play this game fair and square (or be hanged)"
LOSER_MSG = "You just lost the Game. Your word is: {} "
WINNER_MSG = "You just won the Game. hooray. im so happy for you. you magnificent beast."
PLAY_AGAIN_MSG = "You won {} games so far. your score is {}. do you want to play again?"
LOSE_STREAK = "You finally lost, after {} games. Do you think you can do better this time? "

""" Part A.1 - helper functions """


# helper functions


def letter_in_word(word, letter):
    """helper function that gets a word as a list of chars returns true if the letter is inside the word list"""
    if letter in word:
        return True
    return False


def letter_position(word_list, letter):
    """ this function returns the position(s) of a letter in word_list"""
    position_list = []
    for letter_pos in range(len(word_list)):
        if word_list[letter_pos] == letter:
            position_list.append(letter_pos)
    return position_list


def correct_letter(word, letter):
    """this function returns a score based of the number of times a letter appears in the word"""
    appearance_list = letter_position(list(word), letter)
    n = len(appearance_list)
    return n * (n + 1) // 2


def correct_word(pattern):
    """ this function returns a score based on the number of missing letter"""
    underscore_count = 0
    for i in pattern:  # counts all the missing letters in the pattern
        if i == '_':
            underscore_count += 1
    n = underscore_count  # using n for easier readability
    return n * (n + 1) // 2


# main function for A.1


def update_word_pattern(word, pattern, letter):
    """ this function gets a word, pattern and a letter and updates the pattern if the letter is in the word """

    word_list = list(word)  # turning the word to a list of chars
    if letter_in_word(word_list, letter):  # checks if the letter is really in the word
        letter_position_list = letter_position(word_list, letter)
        updated_pattern_list = list(pattern)
        for pos in letter_position_list:
            updated_pattern_list[pos] = letter
        updated_pattern = ''.join(map(str, updated_pattern_list))
        return updated_pattern

    else:
        return pattern


# print(update_word_pattern('apple','_'*len('apple'),'*'))

""" Part B - creating a filter function for 'cheating' """


def possible_word(word, pattern, wrong_guess_lst):
    """this function compare a word to a pattern to check if it can fit in the pattern,
     returns True if the word fits the criteria """

    possible_word_length = len(pattern)
    possible_letters = [c for c in list(ABC) if c not in wrong_guess_lst]
    possible_letters.insert(0, '_')
    if len(word) != possible_word_length:
        return False
    for letter in range(possible_word_length):
        if word[letter] not in possible_letters:
            return False
        if word[letter] == pattern[letter] or pattern[letter] == '_':
            continue
        return False
    return True


# print(possible_word('abcd', 'a___', ['e','f','g']))

def filter_words_list(words, pattern, wrong_guess_lst):
    """ this function gets a list of words, filter the possible right words that fit the pattern
     and then return a list of possible words that fit the criteria """

    possible_words = []
    for word in words:
        if possible_word(word, pattern, wrong_guess_lst):
            possible_words.append(word)
    return possible_words


# print(filter_words_list(['aaa','aac','aad','aaaa','aa'], 'a__', ['g', 'd']))


""" Part A.2  - single game function """


def run_single_game(word_list, score):
    """this function runs a single game of hangman and returns the score of the player in the end"""

    # initializing the game

    word = hangman_helper.get_random_word(word_list)
    wrong_guesses = []
    pattern = '_' * len(word)
    msg = STARTING_MSG


    # playing the game
    while word != pattern and score > 0:  # the games run until the player gets the word or lose all his points
        hangman_helper.display_state(pattern, wrong_guesses, score, msg)
        msg = ""
        input_type, current_input = hangman_helper.get_input()
        if input_type == LETTER:  # if the user entered a letter
            if current_input not in ABC:  # skips the iteration if the letter is invalid
                msg = INVALID_LETTER
                continue
            if current_input in pattern or current_input in wrong_guesses:
                msg = SAME_LETTER_AGAIN
                continue
            else:
                score -= 1
                if letter_in_word(word, current_input):  # using the letter in word func to check if valid guess
                    pattern = update_word_pattern(word, pattern, current_input)
                    score += correct_letter(word, current_input)
                else:
                    wrong_guesses.append(current_input)
                continue

        elif input_type == WORD:  # if the user entered a word
            score -= 1
            if current_input == str(word):
                score += correct_word(pattern)
                return score

        elif input_type == HINT:  # the user wants a hint
            if score > 1:
                score -= 1
            hints_list = filter_words_list(word_list, pattern, wrong_guesses)
            if len(hints_list) > HINT_LENGTH:  # if the size of the hint list is larger than HINT_LENGTH
                # the hints list, get shortened to fit it.
                n = len(hints_list)
                sub_hint_list = [hints_list[0], hints_list[(2 * n) // HINT_LENGTH],
                                 hints_list[(HINT_LENGTH - 1) * n // HINT_LENGTH]]
                hints_list = sub_hint_list
            hangman_helper.show_suggestions(hints_list)
            if score == 1:
                score -= 1
            continue
    if score == 0:  # the player lost the Game
        hangman_helper.display_state(pattern, wrong_guesses, score, LOSER_MSG.format(word))
    elif word == pattern:  # the player won the Game
        hangman_helper.display_state(pattern, wrong_guesses, score, WINNER_MSG)
    return score


""" part A.3 """


def main():
    """ the main function for hangman2.py"""
    possible_words_list = hangman_helper.load_words()
    game_count = 0
    player_score = run_single_game(possible_words_list, POINTS_INITIAL)
    while player_score >= 0:
        game_count += 1
        if hangman_helper.play_again(PLAY_AGAIN_MSG.format(game_count, player_score)):
            player_score = run_single_game(possible_words_list, player_score)
        else:
            return
        if player_score == 0:
            if hangman_helper.play_again(LOSE_STREAK.format(game_count)):
                game_count = 0
                player_score = run_single_game(possible_words_list, POINTS_INITIAL)
                continue
            else:
                return


""" Running main """

if __name__ == "__main__":
    main()
