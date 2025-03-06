#################################################################
# FILE : game.py
# WRITER : Yotam Gaash , Gaash , [REDACTED]
# EXERCISE : intro2cs1 ex9 2021
# DESCRIPTION: This class creates a Game.
#              of recursion.
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
#################################################################

class Game:
    """
    this Class implements the Rush Hour game, using a Board object and cars, it receives an instruction file
    and places cars on the board accordingly. each turn the user enter a car name and a move he wish to perform
    the game ends when either the player has entered '!' or when a car has reached the target location.
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self._board = board
        self.__load_cars()
        pass

    def __load_cars(self):
        """
        a helper function that checks the validity of the cars from the json file before adding them
        to the board.

        :param car_dict: a car dictionary received from the json file
        :return: none
        """
        car_dict = load_json(sys.argv[1])
        valid_names = ('Y', 'B', 'G', 'W', 'R', 'O')
        valid_length = (2, 3, 4)
        valid_orientation = (1, 0)
        for car in car_dict:
            if car in valid_names and int(car_dict[car][0]) in valid_length\
            and int(car_dict[car][2]) in valid_orientation:
                new_car = Car(car, car_dict[car][0], tuple(car_dict[car][1]), car_dict[car][2])
                self._board.add_car(new_car)
        return

    def __valid_input(self, user_input):
        if len(user_input) == 3 and list(user_input)[1] == ',':
            return True
        return False

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        print(self._board)
        car_name, movekey = None, None
        user_input = input("enter the name of the car you want to move and the direction to move it:\n")
        if user_input == '!':
            return False
        if self.__valid_input(user_input):
            car_name, movekey = user_input.split(",")
        while not self._board.move_car(car_name, movekey):

            print("Invalid input, please enter a legal move from this list:")
            print(self._board.possible_moves())
            user_input = input()
            if user_input == '!':
                return False
            if self.__valid_input(user_input):
                car_name, movekey = user_input.split(",")
        return True

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print("Welcome to the Rush Hour game! \nEach turn you can move one car by typing its name and "
              "the move you wish to perform. \n"
              "You win when a car gets to the the exit coordinate.\nYou can terminate the game"
              "at any point by typing '!' ")
        exit_coordinates = self._board.target_location()
        while not self._board.cell_content(exit_coordinates):  # the target location is empty
            if not self.__single_turn():
                print("leaving so soon, what a shame.")
                return
        print("Congratulations! You have won!")


if __name__== "__main__":
    from car import Car
    from board import Board
    from helper import load_json
    import sys
    board = Board()
    game = Game(board)
    game.play()
    sys.exit()


