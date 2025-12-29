from enum import Enum

GRID_SIZE = 16

CENTER_SIZE = 2

"""
Walls along the center 4 squares to start
"""
VERTICAL_WALLS_START_STATE = 108892018949695039453121004136991178096640
HORIZONTAL_WALLS_START_STATE = 130668428928063984375413354889719870128128

class Color(Enum):
    RED = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3


class GameBoard(object):
    """
    The pieces are represnted on a 16x16 grid

    Each piece's position is a pair of (x, y) coordinates, meaning it can be
    represented by a 8bit integers

    All pieces combined, therefore, can be represented as a 32-bit integer
    with the 0th->7th bits representing the red piece, 8th->15th bits representing
    the blue piece, 16th->23rd bits representing the green piece, and 24th->31st bits
    representing the yellow piece.
    """
    pieces: int

    target_color: Color

    """
    8bit int representing the target position
    """
    target: int

    """
    The vertical wall bitmap stores the x,y coordinates which have a wall to
    their right. Though technically the 16th column cannot have a wall to its right,
    its simpler to just represent this with a 16x16 grid
    """
    vertical_walls: int
    """
    Horizontal walls bitmap stores the x,y coordinates which have a wall below them

    It could benefit from the same optimization as the vertical walls above
    """
    horizontal_walls: int

    def __init__(self, vertical_walls, horizontal_walls) -> None:
        self.vertical_walls = vertical_walls
        self.horizontal_walls = horizontal_walls
