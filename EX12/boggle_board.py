
from typing import List, Tuple, Optional


class Board:
    """
    This class creates a Board object to be used in the game. the board contains a 2D list of letters.

    """

    NEIGHBORS_DICT = {
        "up_left": (-1,-1),
        "up": (-1, 0),
        "up_right": (-1, 1),
        "left": (0,-1),
        "right": (0,1),
        "down_left": (1,-1),
        "down": (1,0),
        "down_right": (1,1)
    }

    def __init__(self, board: List[List[str]]):
        self._board = board
        self.board_height = len(board)
        self.board_width = len(board[0])

    def __str__(self):
        board_str = '_'*16 + '\n'
        for row in range(self.board_height):
            board_str += '| '
            for col in range(self.board_width):
                board_str += self.get_letter_at_cord((row,col),) + ' | '
            board_str += '\n' + '_'*16 + '\n'
        return board_str

    def valid_cord(self, cord:Tuple[int, int]) -> bool:
        """
        checks if a given cord is inside the board
        :param cord: a cord representing a row and a column
        :return: True of the cord is within the board False otherwise
        """
        return (0 <= cord[0] < len(self._board)) and (0 <= cord[1] < len(self._board[0]))

    def get_neighbors(self, cord: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        this method returns all the neighbor cords of a given cord, for each valid neighbor of the cord.
        :param cord: a cord on the board
        :return: a list of all the valid neighbor cords of the given cord
        """
        neighbors_list = []
        for neighbor in self.NEIGHBORS_DICT:
            cord_neighbor = (cord[0] + self.NEIGHBORS_DICT[neighbor][0], cord[1] + self.NEIGHBORS_DICT[neighbor][1])
            if self.valid_cord(cord_neighbor):
                neighbors_list.append(cord_neighbor)

        return neighbors_list

    def get_letter_at_cord(self, cord: Tuple[int, int]) -> Optional[str]:
        """
        this method returns the letter in the cord position if the cord is inside the bord
        :param cord: a given cord
        :return: the letter inside the cord position.
        """
        if self.valid_cord(cord):
            return self._board[cord[0]][cord[1]]
        return None


if __name__ == '__main__':
    pass


