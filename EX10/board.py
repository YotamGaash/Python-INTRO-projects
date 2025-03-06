##############################################################################
# FILE: board.py
# EXERCISE: Intro2cs ex10 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash, Ron Kat ron.kat2mail [REDACTED]
# DESCRIPTION:this file implements the Bomb class to create a bomb object.
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
##############################################################################

from typing import Tuple, List, Dict, Any, Optional


class Board:

    def __init__(self, height, width, snake):

        self.width = width
        self.height = height
        self.snake = snake
        self.apples = []
        self.bomb = None

    def num_of_cells(self) -> int:
        """ This function returns the coordinates of all the cells in this board
        :return: list of coordinates
        """
        return self.height * self.width

    def get_locations_dict(self) -> Dict[Tuple[int, int], str]:
        """
        this function returns a dictionary contains cells and their content
        used in two cases:
        1. for drawing the board every round
        2. for check valid addition of apples and bomb objects to the board (threw get_cell_content)
        not used to check collisions!
        """
        locations_dict = dict()

        for apple in self.apples:
            if apple.get_apple_pos() not in locations_dict:
                locations_dict[apple.get_apple_pos()] = "A"

        for snake_pos in self.snake.get_snake_pos():
            if snake_pos not in locations_dict:
                locations_dict[snake_pos] = "S"

        if self.bomb:
            if self.bomb.get_status() == "Waiting":
                locations_dict[self.bomb.get_position()] = "B"
            if self.bomb.get_status() == "Exploding":
                for pos in self.bomb.explosion_cord_list():
                    locations_dict[pos] = "E"

        return locations_dict

    def get_cell_content(self, cell_coordinates) -> [str]:
        """
        gets position and returns cell content
        """
        locations_dict = self.get_locations_dict()
        if cell_coordinates in locations_dict:
            return locations_dict[cell_coordinates]
        else:
            return None

    def cord_in_board(self, cord: Tuple[int, int]) -> bool:
        """
        checks if a coordinate is outside the board
        :param cord: a given coordinate
        :return: True if it is outside the board, False otherwise
        """
        return not ((0 <= cord[0] < self.height) and (0 <= cord[1] < self.width))

    def ending_game_collisions_check(self) -> bool:
        """
        func checks if snake did an ending game collision
        (went out of range,killed by explosion, collided with bomb, killed himself)
        return True if it does
        """
        for pos in self.snake.get_snake_pos():
            # checks if went out of range
            if self.cord_in_board(pos):
                self.snake.decapitate_head()
                return True

            if len(self.snake.get_snake_pos()) > len(set(self.snake.get_snake_pos())):
                self.snake.decapitate_head()
                return True

            # checks collisions with bombs
            if self.bomb.get_status() == "Waiting":
                if pos == self.bomb.get_position():
                    self.snake.decapitate_head()
                    return True
        return False

    def snake_exploded(self) -> bool:
        """
        checks if the snake was hit by the bomb explosion.
        :return: True if the snake has died horribly, False otherwise.
        """
        if self.bomb.get_status() == "Exploding":
            for pos in self.snake.get_snake_pos():
                for bomb_pos in self.bomb.explosion_cord_list():
                    if pos == bomb_pos:
                        return True
        return False

    def add_apple(self, apple) -> bool:
        """
        checks if an apple can be added in this place. if it does, adds it and return TRUE
        else return False
        """
        if self.get_cell_content(apple.get_apple_pos()) is not None:
            return False
        self.apples.append(apple)
        return True

    def add_bomb(self, bomb) -> bool:
        """
        checks if an apple can be added in this place. if it does add it and return TRUE
        else return False
        """
        if self.get_cell_content(bomb.get_position()) is not None:
            return False
        self.bomb = bomb
        return True

    def apple_devoured(self) -> int:
        """
        if an apple has been eaten returns apples score and removes the apple from the board
        """
        score = 0
        for apple in self.apples:
            for pos in self.snake.get_snake_pos():
                if apple.get_apple_pos() == pos:
                    score = apple.get_apple_score()
                    self.remove_apple(apple)
                    break
        return score

    def remove_apple(self, apple) -> None:
        """
        Removes an apple object from the apple list
        :param apple: an apple object
        :return:
        """
        self.apples.remove(apple)

    def apple_exploded(self) -> None:
        """
        check if apple exploded by bomb. if True, removes apple
        """
        if self.bomb.get_status() != "Exploding":
            return
        for apple in self.apples:
            for pos in self.bomb.explosion_cord_list():
                if apple.get_apple_pos() == pos:
                    self.remove_apple(apple)

    def get_apples(self) -> List[Any]:
        """
        return the board's apple list
        """
        return self.apples

    def remove_bomb(self) -> None:
        """
        remove current bomb from board
        """
        self.bomb = None

    def explosion_out_of_range(self) -> bool:
        """
        func returns True if explosion out of range and remove bomb
        otherwise returns false
        used in snake_main when bomb
        """
        pos_list = self.bomb.explosion_cord_list()
        for pos in pos_list:
            if self.cord_in_board(pos):
                self.remove_bomb()
                return True
        return False
