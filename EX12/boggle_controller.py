##############################################################################
# FILE: boggle_controller.py
# EXERCISE: Intro2cs ex12 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash, Samuel Hayat [REDACTED]
# DESCRIPTION: this is the main file for the boggle game
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
##############################################################################
from typing import Tuple
from ex12_utils import is_valid_path
from boggle_gui import *
from boggle_board import Board
from boggle_board_randomizer import randomize_board


class Controller:
    """
    This is the controller class for the Boggle game.
    In this class we bind the gui and the logic of the game together.

    """

    """ ~~~~ Constants ~~~~"""

    WORD_DICT_FILE = "boggle_dict.txt"
    GAME_TIME = 180
    INITIAL_SCORE = 0

    def __init__(self, root) -> None:
    
        self.root = root
        self.ui = Boogle_UI(root)
        # self.game_ended = False
    
    def initial_display(self) -> None:
        """
        calling for the ui element of the starting menu
        :return:
        """
        self.ui.started_menu(self.game)

    def game(self) -> Tuple[bool, int, List]:
        """
        this method binds functions from the logic to the main game gui element.
        :return:
        """
        self.game_intialisation()

        self.ui.actual_game(board=self.board._board, score=self.INITIAL_SCORE, timer= self.GAME_TIME,
        create_button_callback=self.on_press_letter_button, reset_button_callback=self.on_press_reset_button, 
        send_button_callback=self.on_press_send_button, game_over_callback= self.game_over)

    def game_intialisation(self) -> None:
        """Its a function that initialise all the data needed to begin a game
        """
        self.board = Board(randomize_board())
        self.timer = 0
        self.current_word = ''
        self.pressed_buttons = {}
        self.tried_words = []
        self.found_words = []
        self.score = 0
        self.current_path = []
        self.words = self.get_word_list()

    def get_word_list(self, word_file=WORD_DICT_FILE) -> List[str]:
        """
        creates a list of strings out of a text file
        :param word_file: the name of the file
        :return: list of all the words in the file.
        """
        word_list = []
        with open(word_file, "r") as f:
            for line in f:
                word_list.extend(line.split())
            f.close()
            return word_list

    def on_press_letter_button(self, letter: str, cords: Tuple[int, int]):
        """
        this function is used as the callback function for each letter
        :param letter:
        :param cords:
        :return:
        """
        if self.current_path:
            valid_cords = self.board.get_neighbors(self.current_path[-1])
        else:
            valid_cords = [(y, x) for y in range(self.board.board_height) for x in range(self.board.board_width)]

        if cords not in self.pressed_buttons and cords in valid_cords:
            self.current_word += letter
            self.ui.current_word_label.configure(text=self.current_word)
            self.pressed_buttons[cords] = letter
            self.current_path.append(cords)
            return True
        
        return False

    def on_press_reset_button(self, button_list, default_color):
        """
        the callable function for the reset button, it clears the button list, current word and current path.
        :param button_list: the list of pressed buttons
        :param default_color: the original buttons color
        :return:
        """

        self.clear_current_word()
        self.clear_pressed_buttons(button_list, default_color)
        self.current_path = []
        self.current_word = ""

    def on_press_send_button(self, button_list, default_color, word_list):
        """
        the callable function for the press_send button, it reset the values of the buttons and path and word lists.
        if the currentword isvalid it updates the score accordingly.
        :param button_list: the list of pressed buttons
        :param default_color: the original letter buttons color
        :param word_list: the list of words aready found
        :return:
        """

        if is_valid_path(self.board,self.current_path,self.words) and self.is_valid_word(self.current_word):
            self.update_score()
            self.found_words.append(self.current_word)

            self.ui.add_to_found_words(word_list, self.current_word)
            green_lights = True

        self.tried_words.append(self.current_word)

        self.clear_pressed_buttons(button_list, default_color)
        
        self.clear_current_word()
    

    def is_valid_word(self, word: str) -> bool:
        """
        checks if the word is in the game's words dictionary and if the word has not been already found by the user.
        :param word: the word to be checked
        :return: True if it is a valid word, False otherwise
        """
        return word in self.words and word not in self.found_words

    def game_over(self):
        self.ui.final_screen(self.score, self.found_words, 
        play_again_callback= self.on_press_play_again, give_up_callback= self.on_press_give_up )

    def on_press_play_again(self):
        def f5():
            self.game()
        return f5

    def on_press_give_up(self):
        def f6():
            self.root.destroy()
        return f6

    def update_score(self):
        self.score += len(self.current_path) ** 2
        self.ui.score_label.configure(text= 'SCORE\n' + str(self.score))

    def clear_current_word(self) -> None:

        self.current_word = ''
        self.current_path = []
        self.ui.current_word_label.configure(text=self.current_word)

    def clear_pressed_buttons(self, button_list, default_color):

        for pressed_button in self.pressed_buttons:
            button_list[pressed_button[0]][pressed_button[1]].configure(bg=default_color)
        self.pressed_buttons = {}
