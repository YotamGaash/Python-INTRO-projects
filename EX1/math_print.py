__Author__ = "Yotam Gaash"
__email__ = "Yotam.Gaosh@mail.huji.ac.il"

#################################################################
# FILE : math_print.py
# WRITER : Yotam Gaash , Gaash , [REDACTED]
# EXERCISE : intro2cse ex1 2020
# DESCRIPTION: A program that prints math
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: none
# NOTES: ...
#################################################################

import math

""" Part A """


def golden_ratio():
    # this function calculates the value of the golden ratio and prints it
    fi = (1 + math.sqrt(5)) / 2
    print(fi)


""" Part B """


def six_squared():
    # this function prints the value of 6 to the power of 2.
    print(6 ** 2)


""" Part C """


def hypotenuse():
    # calculates the lenght of the hypotenuse in a right angle triangle
    a, b = 12, 5  # legths of the legs
    c = math.sqrt(a ** 2 + b ** 2)  # using pythagoras theorem
    print(c)


""" Part D """


def pi():
    # prints the value of PI
    print(math.pi)


""" Part E """


def e():
    # prints the value of e
    print(math.e)


""" part F """


def squares_area():
    # this function prints the areas of squares with edges from the length of 1 to 10
    for i in range(10):
        if i < 9:
            print(((i + 1) ** 2), end=" ")
    print(((i + 1) ** 2))


""" Main """

if __name__ == "__main__":
    golden_ratio()
    six_squared()
    hypotenuse()
    pi()
    e()
    squares_area()
