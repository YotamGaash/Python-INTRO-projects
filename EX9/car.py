#################################################################
# FILE : board.py
# WRITER : Yotam Gaash , Gaash , [REDACTED]
# EXERCISE : intro2cs1 ex9 2021
# DESCRIPTION: This class creates a car object
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
#################################################################

class Car:
    """
    This class creates a car object, the car has a name, length, a location on the board and an orientation.
    based on its orientation the car is capable of moving one "square" in the matching axis.
    the class has several methods related to the car movement.
    """
    def __init__(self, name: str, length: int, location: list, orientation: int):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self._name = name
        self._length = length
        self._location = location
        self._orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        cord_list = []
        row_cord, col_cord = self._location
        for i in range(self._length):
            if self._orientation: # horizontal
                cord_list.append((row_cord, col_cord + i))
            else:  # vertical car
                cord_list.append((row_cord + i, col_cord))
        return cord_list

    def valid_params(self):
        """
        checks if the parameters of the car are valid.
        :return: returns True if they are valid, False otherwise.
        """
        valid_names = ('Y','B','G','W','R')
        valid_length = (2, 3, 4)
        valid_orientation = (1, 0)
        if self._name in valid_names and self._length in valid_length and self._orientation in valid_orientation:
            return True
        return False

    def possible_moves(self):

        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """

        vertical_movement_dict = {
                                'u' : " the car moves up",
                                'd' : " the car moves down",
                                }
        horizontal_movement_dict = {
                                    'l': "the car moves left",
                                    'r': "the car moves right"
                                   }
        if self._orientation:  # horizontal
            return horizontal_movement_dict
        else:  # vertical
            return vertical_movement_dict


    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """

        movement_dict = {
                        'u': (self.car_coordinates()[0][0] + -1, self.car_coordinates()[0][1]),
                        'd': (self.car_coordinates()[-1][0] + 1, self.car_coordinates()[-1][1]),
                        'r': (self.car_coordinates()[-1][0], self.car_coordinates()[-1][1] + 1),
                        'l': (self.car_coordinates()[0][0], self.car_coordinates()[0][1] - 1)
                        }
        return [movement_dict[movekey]]


    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        movement_dict = {
                        'u': (-1,0),
                        'd': (1,0),
                        'r': (0,1),
                        'l': (0,-1)
        }
        row_cord, col_cord = self._location
        if movekey in self.possible_moves():
            self._location = (row_cord + movement_dict[movekey][0],
                              col_cord + movement_dict[movekey][1])
            return True
        else:
            return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self._name



