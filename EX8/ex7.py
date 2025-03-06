##############################################################################
# FILE: ex7.py
# EXERCISE: Intro2cs ex7 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash
# DESCRIPTION: This file contains recursive function that contain recursive functions that contains recursive funct...
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
##############################################################################

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

from ex7_helper import *
from typing import Any, List

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

EMPTY_LIST: List[Any] = []

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def mult(x: float, y: int) -> float:
    """
    this function multiples two numbers using a recursion
    :param x: an arbitrary float number
    :param y: a non negative int by which x is multiplied
    :return: either the mult function or a float value.
    """

    if y <= 1:
        return x
    return add(x, mult(x, subtract_1(y)))


def is_even(n: int) -> bool:
    """
    this functions checks if a number is even or odd using recursion
    :param n: a number we want to check
    :return: either it returns true/fasle or it returns itself
    """
    if n == 1:  # one is odd
        return False
    elif n == 0:  # zero is even
        return True
    else:
        return is_even(subtract_1(subtract_1(n)))  # returning the number minus 2 to be checked for oddness


def log_mult(x: float, y: int) -> float:
    """
    this function preforms a multiplication of two number in a logarithmic runtime.
    each step the function return itself with y divided by two if its even or divided by two, with one added
    if its odd. the function ends the recursion if y is either one or zero.
    :param x:  an arbitrary float number
    :param y: a non negative int by which x is multiplied
    :return: either the log_mult function or a float value.
    """

    if y == 1 or y == 0:
        return x
    elif is_odd(y):
        return add(log_mult(x, int(add(divide_by_2(y), 1))), int(log_mult(x, int((divide_by_2(y))))))
    else:
        return add(log_mult(x, divide_by_2(y)), (log_mult(x, divide_by_2(y))))


def is_power(b: int, x: int) -> bool:
    """
    this function checks if b by the power of some number is equal to x.
    each step the function checks if b multiplied by itself is equal to x. if b is bigger than x
    the function returns False
    :param b: the number we want to check to be a root of x
    :param x: an integer
    :return: the function
    """

    def _is_power_helper(original_b: int, b: int, x: int) -> bool:
        """
        an helper function that uses the original value of 'b' and in each step it multiply b by this value
        :param original_b: the 'b' from the is_power function
        :param b: a new 'b' we want to check to be a root of x
        :param x: the 'x' from the is_power function
        :return: True if b equals x, False if b is bigger than x, returns itself otherwise
        """
        if b > x:
            return False
        elif b == x:
            return True
        else:
            return _is_power_helper(original_b, int(log_mult(original_b, int(b))), x)

    if b == 1 and x != 1:  # one equals to it's root (or power)
        return False
    return _is_power_helper(b, b, x)


def reverse(s: str) -> str:
    """
    reversing the order of chars in a string.
    :param s: a string we wish to reverse
    :return: a reversed string
    """

    def _reverse_helper(s: str, n: int) -> str:
        """
        this function adds the chars of s in reverse order into a string
        :param s: the original string from the reverse function
        :param n: the index of the char to be appended to the string
        :return: the reversed string
        """
        if n == len(s) - 1:
            return s[n]
        return append_to_end(_reverse_helper(s, n + 1), s[n])

    return str(_reverse_helper(s, 0))


def play_hanoi(hanoi: Any, n: int, src: Any, dst: Any, temp: Any) -> None:
    """
    Using the hanoi_game file, this function implements a recursive solution to the game. the solution has
    three parts - moving all the discs but the largest to the temp pole. moving the largest disc to the dest pole.
    and lastly moving all the discs from the temp pole to the dst pole.

    :param hanoi: an object from the class hanoi
    :param n: the number of discs in the game
    :param src: a source dist we wish to move
    :param dst: the destination for the chosen disk
    :param temp: a temp pole
    :return: None
    """
    if n <= 0:
        return

    if n == 1:  # moving the last disc to the chosen destination
        hanoi.move(src, dst)
        return

    play_hanoi(hanoi, n - 1, src, temp, dst)
    hanoi.move(src, dst)  # moves all the disks but one to a temp pile
    play_hanoi(hanoi, n - 1, temp, dst, src)


def number_of_ones(n: int) -> int:
    """
    this functions how many times the digit "one" appears in all the numbers that are smaller or equal
     to a chosen number. each iteration the function returns the number of ones that appeared
     so far plus the number of ones in the current number given to the function.

    :param n: an int
    :return: the number of times the digit one appeared overall
    """

    def _ones_in_a_number(m: int, sum_of_ones: int) -> int:
        """
        calculates how many times "one" appears in a given number.
        each step the function checks if the reminder of the number divided by 10 equals to "one"
        and the recursion ends when the number is smaller than 10.
        :param m: the number we want to check
        :param sum_of_ones: the number of times "one" has appeared so far
        :return: the number of times one has appeared overall
        """
        if m < 10:
            if m == 1:
                return sum_of_ones + 1
            return sum_of_ones
        elif m % 10 == 1:
            sum_of_ones += 1
        return _ones_in_a_number(m // 10, sum_of_ones)

    if n == 1:
        return 1
    if n < 1:
        return 0

    return number_of_ones(n - 1) + _ones_in_a_number(n, 0)


def compare_2d_lists(l1: List[List[int]], l2: List[List[int]]) -> bool:
    """
    this function compares two 2D lists of ints to check if they are identical.
    :param l1: a list of lists of ints
    :param l2:a second list of lists of ints
    :return: True if the lists are equal, False otherwise
    """

    def _compare_by_index(index: int, mini_l1: List[int], mini_l2: List[int]) -> bool:
        """
        checks if the numbers in a certain index of the lists is equal
        :param index: the index of the number to be checked
        :param mini_l1:
        :param mini_l2:
        :return:
        """

        if len(mini_l1) is not len(mini_l2):
            return False
        elif index >= len(mini_l1):
            return True
        elif mini_l1[index] == mini_l2[index]:
            return _compare_by_index(index + 1, mini_l1, mini_l2)

        return False

    def _compare_2d_list_helper(i: int, l1: List[List[int]], l2: List[List[int]]) -> bool:
        """
        a helper function that checks each time if two inner lists are equal using the check_by_index function.
        it iterates to the next index if they are, or returns false if they aren't.
        :param i: an index for the inner lists
        :param l1: a list of lists of ints
        :param l2: a second list of lists of ints
        :return: True if the lists are equal. False otherwise
        """
        if len(l1) is not len(l2):
            return False
        elif i >= len(l1):
            return True
        elif _compare_by_index(i, l1[i], l2[i]):
            return _compare_2d_list_helper(i + 1, l1, l2)

        return False

    return _compare_2d_list_helper(0, l1, l2)


def magic_list(n: int) -> List[Any]:
    """
    Creates a Von Neumann ordinal numbers as a series of  empty lists
    :param n: the ordinal which we wish to represent
    :return: a list of an arbitrary number of lists of empty lists
    """

    if n == 0:
        return EMPTY_LIST
    sub_magical_list = [magic_list(n - 1)][:]
    return (magic_list(n - 1)[:]) + sub_magical_list[:]


for i in range(5):
    print([f"{x}" for x in (magic_list(i))], '\n__________________________________\n')
