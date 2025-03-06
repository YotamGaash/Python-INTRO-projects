#######################################################
#                  Exercise 2 Tests                   #
#                    Instructions                     #
#   1. Move this file the to exercise folder          #
#   2. Make sure there aren't any function calls      #
#      in your exercise files                         #
#   3. Run this file and check for errors or success  #
#######################################################


from calculate_mathematical_expression import *
from largest_and_smallest import *
from quadratic_equation import *
from temperature import *

assert calculate_from_string("10 : 2") == 5.0
assert calculate_from_string("10 : -2") == -5.0
assert calculate_from_string("-10 : -2") == 5.0
assert calculate_from_string("-10 : 2") == -5.0
assert calculate_from_string("10 + 2") == 12.0
assert calculate_from_string("100 - 39.3") == 60.7
assert calculate_from_string("5 : 2") == 2.5
assert calculate_from_string("5 : 0") is None
assert calculate_from_string("10 333 2") is None
assert calculate_from_string("10 ^ 2") is None

assert largest_and_smallest(5, 1, 10) == (10, 1)
assert largest_and_smallest(2.5, 2.5, 7) == (7, 2.5)
assert largest_and_smallest(7, 2.5, 2.5) == (7, 2.5)
assert largest_and_smallest(-5, -5, -5) == (-5, -5)
assert largest_and_smallest(10, 0, -2) == (10, -2)
assert check_largest_and_smallest() is True

assert quadratic_equation(1, 1.5, -1) == (0.5, -2)
assert quadratic_equation(1, -8, 16) == (4, None)
assert quadratic_equation(1, -2, 34.5) == (None, None)
assert quadratic_equation(4, -12, 9) == (3 / 2, None)

assert is_it_summer_yet(26, 38, 90, 20) is True
assert is_it_summer_yet(10, 10, 10, 10) is False
assert is_it_summer_yet(10, 11, 10, 11) is True
assert is_it_summer_yet(-1, -9, 0, 1) is True
assert is_it_summer_yet(0, 90, 0, 1) is True

print("All tests passed")
