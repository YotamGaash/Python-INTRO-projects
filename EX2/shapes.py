__Author__ = "Yotam Gaash"
__email__ = "Yotam.Gaosh@mail.huji.ac.il"

#################################################################
# FILE : shapes.py
# WRITER : Yotam Gaash , Gaash , [REDACTED]
# EXERCISE : intro2cs1 ex2 2021
# DESCRIPTION: This program helps Harry with his geometry homework
# in determination of the toughness of spells
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: none
# NOTES: ...
#################################################################


import math

"""magic is real"""

PI = math.pi
CIRCLE = 1
RECTANGLE = 2
TRIANGLE = 3
TWO = 2
TRI_CO_EF = math.sqrt(3) / 4  # the coefficient of a symmetric triangle area formula

""" part F """

"""helper functions"""


def circle_area(radius):
    """this function returns the area of a circle given a radius"""
    return PI * (radius ** TWO)


def rectangle_area(side_a, side_b):
    """this function returns the area of a rectangle given two sides"""
    return side_a * side_b


def triangle_area(edge):
    """this function returns the area of a symmetric triangle given the one edge"""
    return TRI_CO_EF * (edge_len ** TWO)


"""main function """


def shape_area():
    """this program calculate the area of a circle, rectangle or a triangle"""
    shape_num = int(input("Choose shape (1=circle, 2=rectangle, 3=triangle): "))
    if shape_num > TRIANGLE or shape_num < CIRCLE:  # returns none if the shape number is invalid
        return None

    if shape_num == CIRCLE:  # calc the area of a circle
        radius = float(input())
        return circle_area(radius)

    if shape_num == RECTANGLE:  # calc the area of a rectangle
        side_a = float(input())
        side_b = float(input())
        return rectangle_area(side_a, side_b)

    if shape_num == TRIANGLE:  # calc the area of a triangle
        edge_len = float(input())
        return triangle_area(edge_len)
