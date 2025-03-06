__Author__ = "Yotam Gaash"
__email__ = "Yotam.Gaosh@mail.huji.ac.il"

#################################################################
# FILE : temperature.py
# WRITER : Yotam Gaash , Gaash , [REDACTED]
# EXERCISE : intro2cs1 ex2 2021
# DESCRIPTION: This program determinate how hot Hagrid wants it to be
# in determination of the toughness of spells
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: none
# NOTES: ...
#################################################################


""" Part G """

"""Magical days"""

MIN_DAYS = 2


def is_it_summer_yet(set_temp, day1_temp, day2_temp, day3_temp):
    """this function gets a set temperature and checks if this temp was reached for atleast two days"""
    temp_day_count = 0
    days = [day1_temp, day2_temp, day3_temp]
    for day in days:
        if float(day) >= set_temp:
            temp_day_count += 1
    if temp_day_count >= MIN_DAYS:  # if there were at least two hot days it is summer
        return True
    return False
