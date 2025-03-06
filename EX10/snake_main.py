##############################################################################
# FILE: snake_main.py
# EXERCISE: Intro2cs ex10 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash, Ron Kat ron.kat2mail [REDACTED]
# DESCRIPTION: The game logic is implemented here. The game runs a while loop until a game ending scenarios occurs
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
##############################################################################


import game_parameters
from apple import Apple
from snake import Snake
from bomb import Bomb
from board import Board
from game_display import GameDisplay
from typing import Optional

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

COLORS_DICT = {"S": "black", "B": "red", "E": "orange", "A": "green"}
APPLE_NUMBER_CONST = 3

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Helper Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def draw_board(gd: GameDisplay, board: Board) -> None:
    """
    Draws all the cells that contain objects from the board's location dictionary
    :param gd: game display object
    :param board: board object
    :return: None
    """
    locations_dict = board.get_locations_dict()
    for location in locations_dict:
        if not board.cord_in_board(location):
            gd.draw_cell(location[1], location[0], COLORS_DICT[locations_dict[location]])


def add_apples_to_board(board: Board) -> None:
    """
    adding apples to board when game starts and when apple has been eaten or exploded
    """
    while True:
        x, y, score = game_parameters.get_random_apple_data()
        apple = Apple(score, x, y)
        if board.add_apple(apple):
            return


def add_new_bomb(board: Board) -> None:
    """
    adding new bomb to board
    (used in start of the game or when bomb exploded)
    """
    x, y, radius, time = game_parameters.get_random_bomb_data()
    bomb = Bomb((y, x), radius, time)
    while True:
        if board.add_bomb(bomb):
            return


def initialize_board(snake: Snake, gd: GameDisplay, game_score: int) -> Board:
    """
    this function sets the initial board for the game
    :param gd: game display object
    :param game_score: the current game score
    :param snake: the snake object
    :return: the board object
    """

    gd.show_score(game_score)
    board = Board(game_parameters.HEIGHT, game_parameters.WIDTH, snake)
    add_new_bomb(board)
    for i in range(APPLE_NUMBER_CONST):
        add_apples_to_board(board)
    return board


def refresh_apples(board: Board) -> None:
    """
    Adds new apples to the board if there are missing apples
    :param board: the game board
    :return: none
    """
    if len(board.get_apples()) < APPLE_NUMBER_CONST:
        for i in range(APPLE_NUMBER_CONST - len(board.get_apples())):
            add_apples_to_board(board)


def key_click_event(key: Optional[str], snake) -> None:
    """
    moves the snake according to the key the user pressed
    :param key: string with the direction  movement of None if no key was pressed
    :param snake: the snake object
    :return:None
    """
    if key:
        snake.move_snake(key)
    else:
        snake.move_snake(snake.snake_dir)


def add_score(board: Board) -> int:
    """
    return the amount of score points to add in the case the snake ate an apple
    :param board: the game board
    :return: the amount of points to be added
    """

    score_points = board.apple_devoured()
    if score_points > 0:
        board.snake.ate_apple()
        return score_points
    else:
        return 0  # zero points added if zero apples have been eaten


def bomb_update(board) -> None:
    """
    update the bomb timer and checks how it affects the other game objects
    :param board:
    :return:
    """

    if board.explosion_out_of_range():
        add_new_bomb(board)
    elif board.bomb.get_status() == "Waiting" or board.bomb.get_status() == "Exploding":
        board.bomb.update_time()
    else:
        add_new_bomb(board)


"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Main Game Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def main_loop(gd: GameDisplay) -> None:
    """
    the main game loop, runs until a game ending event has occurred.
    :param gd: A game display object
    :return: None
    """

    game_score = 0
    board = initialize_board(Snake(), gd, game_score)
    draw_board(gd, board)
    board.bomb.update_time()
    gd.end_round()

    while True:  # the main game loop
        key_click_event(gd.get_key_clicked(), board.snake)  # get input from the user and moves the snake accordingly

        if board.ending_game_collisions_check():  # check if a game ending collision has occurred
            draw_board(gd, board)
            gd.end_round()
            break

        board.apple_exploded()  # check if an apple exploded
        bomb_update(board)  # updating the bomb status

        if board.snake_exploded():  # checks if the snake was hit by the bomb explosion
            draw_board(gd, board)
            gd.end_round()
            break

        game_score += add_score(board)  # updating the score
        gd.show_score(game_score)

        if len(board.snake.get_snake_pos()) + 4 == board.num_of_cells():  # ends the game if the board is full
            break

        refresh_apples(board)
        draw_board(gd, board)
        gd.end_round()



#            /^\/^\
#          _|__|  O|
# \/     /~     \_/ \   Snake to meet you
#  \____|__________/  \
#         \_______      \
#                 `\     \                 \
#                   |     |                  \
#                  /      /                    \
#                 /     /                       \\
#               /      /                         \ \
#              /     /                            \  \
#            /     /             _----_            \   \
#           /     /           _-~      ~-_         |   |
#          (      (        _-~    _--_    ~-_     _/   |
#           \      ~-____-~    _-~    ~-_    ~-_-~    /
#             ~-_           _-~          ~-_       _-~
#                ~--______-~                ~-___-~