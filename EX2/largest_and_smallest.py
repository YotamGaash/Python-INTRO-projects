__Author__ = "Yotam Gaash"
__email__ = "Yotam.Gaosh@mail.huji.ac.il"

#################################################################
# FILE : largest_and_smallest.py
# WRITER : Yotam Gaash , Gaash , [REDACTED]
# EXERCISE : intro2cs1 ex2 2021
# DESCRIPTION: A program the largest and smallest numbers from a list of 3 numbers
# in determination of the toughness of spells
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: none
# NOTES: ...
#################################################################

"""magic test"""

REQ_TESTS = 5  # number of tests required for check function

"""" part C """


def largest_and_smallest(num_a, num_b, num_c):
    """A function that recieves three numbers and returns the largest and the smallest ones"""
    max_val = num_a  # setting the starting values of min and max values to the first number
    min_val = num_a
    num_list = [num_a, num_b, num_c]  # arranging the numbers to a list for the for loop

    for number in range(len(num_list) - 1):
        if num_list[number + 1] >= max_val:  # if a value in num list is bigger than the previous one max value takes it
            max_val = num_list[number + 1]
        if num_list[number + 1] <= min_val:  # if the value is smaller than the previous one min value takes it
            min_val = num_list[number + 1]
    return max_val, min_val


""" Part I """


def check_largest_and_smallest():
    """checks if largest and smallest works using 5 different inputs"""
    check_count = 0
    test_tuple = ([17, 1, 6], [1, 17, 6], [1, 1, 2], [0, 0.1, 0.01], [1, -1, 0])  # 5 different tests as lists
    # in a tuple
    expected_results_tuple = ((17, 1), (17, 1), (2, 1), (0.1, 0), (1, -1))  # expected results as tuple tuples
    for test_num in range(len(test_tuple)):
        num1, num2, num3 = test_tuple[test_num]
        if largest_and_smallest(num1, num2, num3) == expected_results_tuple[test_num]:
            check_count += 1
    if check_count == REQ_TESTS:
        return True
    else:
        return False
