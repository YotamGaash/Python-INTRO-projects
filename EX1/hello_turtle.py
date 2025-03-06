__Author__ = "Yotam Gaash"
__email__ = "Yotam.Gaosh@mail.huji.ac.il"

#################################################################
# FILE : hello_turtle.py
# WRITER : Yotam Gaash , Gaash , [REDACTED]
# EXERCISE : intro2cs1 ex1 2021
# DESCRIPTION: A program that abuses turtles to draw a flower garden
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: none
# NOTES: ...
#################################################################


import turtle

"""Magic Numbers AKA Globals"""

RAD_PI = 180
RAD_HALF_PI = 90  # using radians as names for degrees
RAD_Q_PI = 45
RAD_HEX_PI = 30
RAD_QH = RAD_Q_PI + RAD_HALF_PI
DISTANCE_UNIT_30 = 30  # pixels as measuring names
DISTANCE_UNIT_100 = 100
DISTANCE_UNIT_150 = 150
DISTANCE_UNIT_200 = 200
PETAL_NUM = 4
TWO = 2  # the magical and mythical number two

""" function used to simplify the use of turtle in the code. """


def turtle_right(degree):
    turtle.right(degree)


def turtle_left(degree):
    turtle.left(degree)


def turtle_forward(distance):
    turtle.forward(distance)


""" Part A"""


def draw_petal():
    """" this function draws a flower petal """
    for side in range(TWO):  # copying the symmetry using for loop
        turtle_forward(DISTANCE_UNIT_30)
        turtle_right(RAD_Q_PI)
        turtle_forward(DISTANCE_UNIT_30)
        turtle_right(RAD_QH)


""" Part B """


def draw_flower():
    """ this function draws a flower using the draw_petal function """
    turtle_left(RAD_Q_PI)
    draw_petal()
    for petal in range(PETAL_NUM - 1):  # using for loop for the last 3 petals
        turtle_left(RAD_HALF_PI)
        draw_petal()
    turtle_left(RAD_QH)
    turtle_forward(DISTANCE_UNIT_150)


""" Part C """


def draw_flower_and_advance():
    """" this function draws a flower and move our little turtle forward """
    draw_flower()
    turtle_right(RAD_HALF_PI)
    turtle.up()
    for i in range(TWO):
        turtle_forward(DISTANCE_UNIT_150)
        turtle_right(RAD_HALF_PI)
    turtle_left(RAD_PI)
    turtle.down()


def draw_flower_bed():
    """" this function draws a flower bed using the draw_flower_and_advance function"""
    turtle.up()
    turtle_forward(DISTANCE_UNIT_200)
    turtle_left(RAD_PI)
    turtle.down()
    for i in range(3):
        draw_flower_and_advance()


# main part
if __name__ == "__main__":
    draw_flower_bed()
    turtle.done
