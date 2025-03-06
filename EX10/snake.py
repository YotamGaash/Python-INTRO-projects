##############################################################################
# FILE: snake.py
# EXERCISE: Intro2cs ex10 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash, Ron Kat ron.kat2mail [REDACTED]
# DESCRIPTION:this file implements the snake class to create a snake object.
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
##############################################################################
from typing import Tuple, List


"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Node Object ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


class SnakeJoint:
    """
    this class creates a Node object for each joint of the snake.
    The snake is implemented as a linked list of joints"""

    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    def get_position(self) -> Tuple[int, int]:
        """
        gets the position from the object data
        :return: the SnakeJoint data
        """
        return self.data


"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Snake class ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


class Snake:

    """
    this class creates the Snake object for the game, the snake is implemented as a linked list.
    """

    """~~~~~~~~~~~~~~~~~~~~~~~~~~ Constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    STARTING_POS = (10, 10)
    INIT_LENGTH = 3
    INIT_DIRECTION = "Up"
    APPLE_GROWTH = 3

    dir_dict = {

        "Up": (1, 0),
        "Down": (-1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    opposite_directions = {"Up": "Down", "Left": "Right", "Right": "Left", "Down": "Up"}

    def __init__(self):

        self.snake_head = SnakeJoint(self.STARTING_POS)
        self.set_initial_snake()
        self.snake_dir = self.INIT_DIRECTION
        self.is_growing = 0

    def set_initial_snake(self) -> None:
        """
        creates an initial snake for the start of the game, given the default snake location
        :return: Nonee
        """
        current_joint = self.snake_head
        for i in range(self.INIT_LENGTH - 1):
            current_joint.next = SnakeJoint((self.STARTING_POS[0] - (i + 1), self.STARTING_POS[1]))
            current_joint = current_joint.next

    def ate_apple(self) -> None:
        """
        adds the constant of the apple growth to the is growing variable, it gets called whenever the snake
        eats an apple
        """
        self.is_growing += self.APPLE_GROWTH

    def decapitate_head(self) -> None:
        """
        removes the head of the snake from the linked list of the snake
        :return: None
        """
        self.snake_head = self.snake_head.next

    def move_snake(self, direction: str) -> None:

        """
        this function moves the snake in a chosen direction, it appends a new head to the snake in the new location
        and deletes the snake tail if the snake is not growing.
        :param direction: The direction of the new movement
        """

        if self._valid_direction(direction):
            self.snake_dir = direction

        x, y = self.snake_head.get_position()
        new_x, new_y = self.dir_dict[self.snake_dir]
        self._new_snake_head((x + new_x, y + new_y))
        self._delete_snake_tail()
        if self.is_growing:
            self.is_growing -= 1

    def _delete_snake_tail(self) -> None:
        """
        this function removes the tail of the snake
        :return:
        """
        if not self.is_growing:
            current_joint = self.snake_head
            while current_joint.next.next is not None:
                current_joint = current_joint.next
            current_joint.next = None

    def _new_snake_head(self, new_pos: Tuple[int, int]) -> None:
        """
        this function inserts a new head to the snake in a given location
        :param new_pos: the position of the new head on the board
        :return: None
        """
        new_head = SnakeJoint(new_pos)
        new_head.next = self.snake_head
        new_head.prev = None

        if self.snake_head is not None:
            self.snake_head.prev = new_head

        self.snake_head = new_head

    def get_snake_pos(self) -> List[Tuple[int, int]]:
        """
        this getter function returns the positions of all the snake joints
        :return: a list of tuples of the snake cords
        """
        coordinates_list = []
        current_joint = self.snake_head
        while current_joint is not None:
            coordinates_list.append(current_joint.data)
            current_joint = current_joint.next

        return coordinates_list

    def _valid_direction(self, direction: str) -> bool:
        """
        checks if the given direction is opposite to the current snake direction
        :param direction: the new direction to check
        :return: False if the directions are opposite, True otherwise.
        """
        if self.snake_dir == self.opposite_directions[direction]:
            return False
        return True

