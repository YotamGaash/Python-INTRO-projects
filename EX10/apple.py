##############################################################################
# FILE: apple.py
# EXERCISE: Intro2cs ex10 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash, Ron Kat ron.kat2mail [REDACTED]
# DESCRIPTION: this file implements the Apple class to create an Apple object.
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
##############################################################################
from typing import Tuple


class Apple:
    """
    This class is used to create an apple object.
    """

    def __init__(self, score: int, x_pos: int, y_pos: int):
        """
        this class creates an apple. gets score and position randomly from game parameters during
        the game
        """
        self.__apple_score = score
        self.__apple_pos = (y_pos, x_pos)

    def get_apple_score(self) -> int:
        """
        this func returns the apples score
        """
        return self.__apple_score

    def get_apple_pos(self) -> Tuple[int, int]:
        """
        this func returns apples position
        """
        return self.__apple_pos



