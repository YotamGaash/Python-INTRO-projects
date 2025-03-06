##############################################################################
# FILE: bomb.py
# EXERCISE: Intro2cs ex10 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash, Ron Kat ron.kat2mail [REDACTED]
# DESCRIPTION:this file implements the Bomb class to create a bomb object.
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
##############################################################################


from typing import List, Tuple


class Bomb:
    WAIT_STATUS = "Waiting"
    EXPLODE_STATUS = "Exploding"
    DEAD_STATUS = "Dead"

    def __init__(self, position, radius, time):

        self._position = position
        self._bomb_status = self.WAIT_STATUS
        self._radius = radius + 1
        self._fuse_time = time
        self._explosion_time = radius
        self._current_radius = 0  # Time till the explosion and the time of the explosion (radius)

    def update_time(self) -> None:
        """
        Calling this function increments the bomb variables in order to simulate bomb life cycle
        """
        if self._fuse_time > 0:  # Happens until the explosion
            self._fuse_time -= 1
            self._bomb_status = self.WAIT_STATUS

        elif self._fuse_time == 0:
            self._bomb_status = self.EXPLODE_STATUS
            self._fuse_time -= 1
            return

        elif self._explosion_time >= 0:  # From the time of the detonation until the blast reach the size of the radius
            self._bomb_status = self.EXPLODE_STATUS
            self._current_radius += 1
            self._explosion_time -= 1
            return

        else:
            self._bomb_status = self.DEAD_STATUS  # the bomb finished its life cycle and needs to be removed

    def get_status(self) -> str:
        """
        Getter method for the bomb status
        :return: the bomb status variable
        """
        return self._bomb_status

    def get_position(self) -> Tuple[int, int]:
        """
        Getter method for the bomb position
        :return: the bomb position variable
        """
        return self._position

    def _explosion_matrix(self, radius: int) -> List[List[Tuple[int, int]]]:
        """

        :param radius: the radius of the explosion
        :return: a 2D list of cords in the radius around the bomb position
        """

        return [[(x, y) for x in range(self._position[0] - radius, self._position[0] + radius + 1)]
                for y in range(self._position[1] - radius, self._position[1] + radius + 1)]

    def _manhattan_dist(self, radius: int, cord: Tuple[int, int]) -> bool:
        """
        this function checks if a certain coordination is in a Manhattan Distance from the bomb position
        :param radius: the radius of the explosion
        :param cord: the cord we want to check
        :return:
        """
        return (abs(self._position[0] - cord[0]) + abs(self._position[1] - cord[1])) == radius

    def explosion_cord_list(self) -> List[Tuple[int, int]]:
        """
        this function returns a list of all the cords in a Manhattan Distance from the bomb position
        :return: a list of the explosion coordination
        """
        # Matrix with all the cords in around the radius from the bomb location
        exp_matrix = self._explosion_matrix(self._current_radius)

        # returns a list consisting only of cords that are in a "Manhattan Distance" from the bomb position
        return [cord for r in exp_matrix for cord in r if
                self._manhattan_dist(self._current_radius, cord)]
