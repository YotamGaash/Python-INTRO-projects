__Author__ = "Yotam Gaash"
__email__ = "Yotam.Gaosh@mail.huji.ac.il"

#################################################################
# FILE : quadratic_equation.py
# WRITER : Yotam Gaash , Gaash , [REDACTED]
# EXERCISE : intro2cs1 ex2 2021
# DESCRIPTION: this program helps Harry's stepbrother solve quadratic equations
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: https://en.wikipedia.org/wiki/Quadratic_formula
# NOTES: in this program I exclude the use of complex numbers.
#################################################################

import math

"""magical nums"""
ZERO = 0
ONE = 1
TWO = 2
FOUR = 4
""" Part D """

"""helper functions"""


def discriminant_finder(a, b, c):
    """using the discriminant of the equation to determinate the number of solutions"""
    return (b ** 2) - (4 * a * c)  # normalized equation as shown in wikipedia (the thing inside the root)


def solution_num(disc):
    """this function determinate the number of real solutions using the discriminant"""
    if disc < ZERO:
        return ZERO
    if disc == ZERO:
        return ONE
    else:
        return TWO


""" helped functions"""


def quadratic_equation(a, b, c):
    """this function receives three parameters of a quad equation and returns the roots of the equation"""
    discriminant = discriminant_finder(a, b, c)
    solutions = solution_num(discriminant)
    if solutions == ZERO:
        return None, None  # no "real" solutions for the equation

    # roots are calculated after making sure the discriminant is not negative to prevent negative square roots
    root1 = (-b + math.sqrt(discriminant)) / (TWO * a)
    root2 = (-b - math.sqrt(discriminant)) / (TWO * a)

    if solutions == ONE:  # if there is only a single solution the function returns it as root1
        # and the second solution as none
        return root1, None  # one solution

    if solutions == TWO:
        return root1, root2  # two solutions


""" Part E"""


def quadratic_equation_user_input():
    """solving a quadratic equation using the function from part D with user input"""
    a, b, c = input("Insert coefficients a, b, and c: ").split()
    a, b, c = float(a), float(b), float(c)  # converting the input to floats

    if a == ZERO:  # a must not equal zero for the equation to be quadratic
        print("The parameter 'a' may not equal 0")
        return
    root1, root2 = quadratic_equation(a, b, c)  # using quadratic_equations function
    solutions = solution_num(discriminant_finder(a, b, c))
    discriminant = b ** 2 - 4 * a * c  # using the discriminant to see how many real solutions the equation has
    if solutions == ZERO:
        print("The equation has no solutions")
        return
    if solutions == ONE:
        print("The equation has 1 solution:", root1)
        return
    if solutions == TWO:
        print("The equation has 2 solutions:", root1, "and", root2)
        return
