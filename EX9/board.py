#################################################################
# FILE : board.py
# WRITER : Yotam Gaash , Gaash , [REDACTED]
# EXERCISE : intro2cs1 ex9 2021
# DESCRIPTION: This class creates a board object
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
#################################################################


class Board:
    """
    this class creates a board object that contain car objects. the board is of fixed
    length. you can add and move cars on the board.
    """

    def __init__(self):
        self._board_size = 7
        self._empty_cell = '_'
        self._car_dict = {}
        self._board = [[self._empty_cell for _ in range(self._board_size)] for _ in range(self._board_size)]
        self._board[3].append(self._empty_cell)  # adding the exit coordinate

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """

        board_str = ""
        for row in range(len(self._board)):
            for col in range(len(self._board)):
                board_str += str(self._board[row][col]) + " "
            board_str += '\n'
        return board_str

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        #In this board, returns a list containing the cells in the square
        #from (0,0) to (6,6) and the target cell (3,7)
        cell_list = [self.target_location()]
        for row in range(len(self._board)):
            for col in range(len(self._board)):
                cell_list.append((row, col))
        return cell_list

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        #From the provided example car_config.json file, the return value could be
        #[('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        moves_list = []
        for car in self._car_dict:
            for move in self._car_dict[car].possible_moves():
                if self._car_dict[car].movement_requirements(move)[0] in self.cell_list() \
                and not self.cell_content(self._car_dict[car].movement_requirements(move)[0]):
                # checks if the move is is for a coordinate inside the board and that the cell is empty
                    moves_list.append((car, move, self._car_dict[car].possible_moves()[move]))
        return moves_list

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return (3,7)

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if self._board[coordinate[0]][coordinate[1]] == self._empty_cell:
            return None
        else:
            return self._board[coordinate[0]][coordinate[1]]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        #Remember to consider all the reasons adding a car can fail.
        #You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"

        car_cords = car.car_coordinates()
        if car.get_name() in self._car_dict:  # there cant be two cars with the same name
            return False
        for cord in car_cords:
            if cord not in self.cell_list():  # the car is not on the board
                return False
            elif self.cell_content(cord):  # the cell is taken by another car
                return False
        self.__place_car(car)
        self._car_dict[car.get_name()] = car
        return True

    def __place_car(self,car):
        """
        places a car on the board
        :param car: car object to place
        :return: none
        """
        for cord in car.car_coordinates():
            self._board[cord[0]][cord[1]] = car.get_name()

    def __erase_car(self, car):
        """
        erases a car from the board
        :param car: car object to erase
        :return: none
        """
        for cord in car.car_coordinates():
            self._board[cord[0]][cord[1]] = self._empty_cell


    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        if name in self._car_dict:
            car = self._car_dict[name]
            if movekey in car.possible_moves():
                if car.movement_requirements(movekey)[0] in self.cell_list() \
                and not self.cell_content(car.movement_requirements(movekey)[0]):
                    self.__erase_car(car)
                    car.move(movekey)
                    self.__place_car(car)
                    return True
        return False



