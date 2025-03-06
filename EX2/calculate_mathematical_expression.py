__Author__ = "Yotam Gaash"
__email__ = "Yotam.Gaosh@mail.huji.ac.il"

#################################################################
# FILE : calculate_mathematical_expression.py
# WRITER : Yotam Gaash , Gaash , [REDACTED]
# EXERCISE : intro2cs ex2 2022
# DESCRIPTION: A program designed to Tony stark with math, and his
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: none
# NOTES: ...
#################################################################


""" CONSTANTS """

VALID_OPS = ('+', '-', '*', '/')  # tuple of valid chars used as arithmetic expressions

"""helper functions"""


def is_valid_op(operator):
    """ helper function that check is the operator is one of the valid four chars """
    if operator in VALID_OPS:
        return True
    else:
        return False


""" part A """


def calculate_mathematical_expression(num1, num2, operator):
    """
    A function that gets two numbers and and an operation char and returns the math expression if it is valid
    :param num1: int/float number
    :param num2: second int/float number
    :param operator: a char describing a math operator
    :return: result of the math expression or none if the operation is invalid
    """
    if not (is_valid_op(operator)):  # returns None if the operator is invalid
        return None
    # return the math expressions determined by the operator
    if operator == VALID_OPS[0]:
        return num1 + num2
    elif operator == VALID_OPS[1]:
        return num1 - num2
    elif operator == VALID_OPS[2]:
        return num1 * num2
    elif operator == VALID_OPS[3]:
        if num2 == 0:  # returns None to prevent a division by zero
            return None
        return num1 / num2


""" Part B """


def calculate_from_string(math_string):
    """
    this function receives math expression as a string and uses the function from part A to return the result"
    :param math_string: string describing a math expression
    :return: the result of the math expression
    """
    num1, operator, num2 = str(math_string).split()  # splits the string to 3 variables
    return calculate_mathematical_expression(float(num1), float(num2), operator)
