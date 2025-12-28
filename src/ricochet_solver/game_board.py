GRID_SIZE = 16

CENTER_SIZE = 2

"""
Walls along the center 4 squares to start
"""
VERTICAL_WALLS_START_STATE = 425365939393319416398289585530533314560
HORIZONTAL_WALLS_START_STATE = 510423550856776670280647936708916019200

class GameBoard(object):
    """
    The board is 16x16 grid, meaning the
    horizontal and vertical walls can each exist
    on 15 lines of 15 units length (the outermost walls are always fully bordered


    Vertical and horizontal walls are each represented with 225-bit (15x15) integers.
    
    For vertical walls, the least-significant bit represents the wall between
    (0,0) and (1,0). The next bit represents the wall between (1,0) and (2,0).
    The 16th bit represents the wall between (0,1) and (1,1), and so on.
    """
    vertical_walls: int
    """
    For horizontal walls, the least-significant bit represents the wall between
    (0,0) and (0,1). The next bit represents the wall between (0,1) and (0,2).
    The 16th bit represents the wall between (1,0) and (1,1), and so on.
    """
    horizontal_walls: int

    def __init__(self) -> None:
        self.vertical_walls = VERTICAL_WALLS_START_STATE
        self.horizontal_walls = HORIZONTAL_WALLS_START_STATE

    def add_horizontal_wall(self, x, y) -> None:
        """
        Note that the x,y coordinates when refering to walls are on a 15x15 grid
        rather than 16x16, since walls exist between cells.
        """
        assert(x < GRID_SIZE - 1)
        assert(x >= 0)

        assert(y < GRID_SIZE - 1)
        assert(y >= 0)

        assert not self._is_uneditable_horizontal_wall_coord(x, y)

        self.horizontal_walls |= (1 << (y * (GRID_SIZE - 1) + x))

    def add_vertical_wall(self, x, y) -> None:
        """
        Note that the x,y coordinates when refering to walls are on a 15x15 grid
        rather than 16x16, since walls exist between cells.
        """
        assert(x < GRID_SIZE - 1)
        assert(x >= 0)

        assert(y < GRID_SIZE - 1)
        assert(y >= 0)

        assert not self._is_uneditable_vertical_wall_coord(x, y)

        self.vertical_walls |= (1 << (y * (GRID_SIZE - 1) + x))

    def remove_horizontal_wall(self, x, y) -> None:
        """
        Note that the x,y coordinates when refering to walls are on a 15x15 grid
        rather than 16x16, since walls exist between cells.
        """
        assert(x < GRID_SIZE - 1)
        assert(x >= 0)

        assert(y < GRID_SIZE - 1)
        assert(y >= 0)

        assert not self._is_uneditable_vertical_wall_coord(x, y)

        self.horizontal_walls &= ~(1 << (y * (GRID_SIZE - 1) + x))

    def remove_vertical_wall(self, x, y) -> None:
        """
        Note that the x,y coordinates when refering to walls are on a 15x15 grid
        rather than 16x16, since walls exist between cells.
        """
        assert(x < GRID_SIZE - 1)
        assert(x >= 0)

        assert(y < GRID_SIZE - 1)
        assert(y >= 0)

        assert not self._is_uneditable_vertical_wall_coord(x, y)

        self.vertical_walls &= ~(1 << (y * (GRID_SIZE - 1) + x))

    def has_horizontal_wall(self, x, y) -> bool:
        """
        Note that the x,y coordinates when refering to walls are on a 15x15 grid
        rather than 16x16, since walls exist between cells.
        """
        assert(x < GRID_SIZE - 1)
        assert(x >= 0)

        assert(y < GRID_SIZE - 1)
        assert(y >= 0)

        return self.horizontal_walls & (1 << (y * (GRID_SIZE - 1) + x)) != 0

    def has_vertical_wall(self, x, y) -> bool:
        """
        Note that the x,y coordinates when refering to walls are on a 15x15 grid
        rather than 16x16, since walls exist between cells.
        """
        assert(x < GRID_SIZE - 1)
        assert(x >= 0)

        assert(y < GRID_SIZE - 1)
        assert(y >= 0)

        return self.vertical_walls & (1 << (y * (GRID_SIZE - 1) + x)) != 0

    def _is_uneditable_vertical_wall_coord(self, x: int, y: int) -> bool:
        return x >= 6 and x <= 8 and y >= 7 and y <= 8

    def _is_uneditable_horizontal_wall_coord(self, x: int, y: int) -> bool:
        return x >= 7 and x <= 8 and y >= 6 and y <= 8
