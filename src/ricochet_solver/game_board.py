
GRID_SIZE = 16

CENTER_SIZE = 2

"""
Walls along the center 4 squares to start
"""
VERTICAL_WALLS_START_STATE = 108892018949695039453121004136991178096640
HORIZONTAL_WALLS_START_STATE = 130668428928063984375413354889719870128128

class BoardBitmap:
    bitmap: int

    def __init__(self, bitmap: int) -> None:
        self.bitmap = bitmap

    @classmethod
    def from_positions(cls, positions: list[tuple[int, int]]):
        bitmap = 0
        for x, y in positions:
            bitmap |= (1 << (y * GRID_SIZE + x))
        return cls(bitmap)

    def scan_right_from(self, x, y) -> int:
        row = self.row(y)

        while x < GRID_SIZE:
            if (row & (1 << x)) != 0:
                return x
            x += 1

        return GRID_SIZE - 1

    def scan_left_from(self, x, y) -> int:
        row = self.row(y)

        while x > 0:
            if (row & (1 << (x - 1))) != 0:
                return x
            x -= 1

        return 0

    def scan_down_from(self, x, y) -> int:
        col = self.column(x)

        while y < GRID_SIZE:
            if (col & (1 << y)) != 0:
                return y
            y += 1

        return GRID_SIZE - 1

    def scan_up_from(self, x, y) -> int:
        col = self.column(x)

        while y > 0:
            if (col & (1 << (y - 1))) != 0:
                return y
            y -= 1

        return 0

    def row(self, y: int) -> int:
        return (self.bitmap >> (y * GRID_SIZE)) & 0b1111111111111111

    def column(self, x: int) -> int:
        row_mask = 2 ** x
        return (
            ((self.bitmap & row_mask) >> x) | 
            (((self.bitmap >> GRID_SIZE) & row_mask) >> x) << 1 |
            (((self.bitmap >> (GRID_SIZE * 2)) & row_mask) >> x) << 2 |
            (((self.bitmap >> (GRID_SIZE * 3)) & row_mask) >> x) << 3 |
            (((self.bitmap >> (GRID_SIZE * 4)) & row_mask) >> x) << 4 |
            (((self.bitmap >> (GRID_SIZE * 5)) & row_mask) >> x) << 5 |
            (((self.bitmap >> (GRID_SIZE * 6)) & row_mask) >> x) << 6 |
            (((self.bitmap >> (GRID_SIZE * 7)) & row_mask) >> x) << 7 |
            (((self.bitmap >> (GRID_SIZE * 8)) & row_mask) >> x) << 8 |
            (((self.bitmap >> (GRID_SIZE * 9)) & row_mask) >> x) << 9 |
            (((self.bitmap >> (GRID_SIZE * 10)) & row_mask) >> x) << 10 |
            (((self.bitmap >> (GRID_SIZE * 11)) & row_mask) >> x) << 11 |
            (((self.bitmap >> (GRID_SIZE * 12)) & row_mask) >> x) << 12 |
            (((self.bitmap >> (GRID_SIZE * 13)) & row_mask) >> x) << 13 |
            (((self.bitmap >> (GRID_SIZE * 14)) & row_mask) >> x) << 14 |
            (((self.bitmap >> (GRID_SIZE * 15)) & row_mask) >> x) << 15
        )

    def has(self, x: int, y: int) -> bool:
        index = y * GRID_SIZE + x
        return (self.bitmap & (1 << index)) != 0

    def __int__(self) -> int:
        return self.bitmap

    def __hash__(self) -> int:
        return self.bitmap

class Board(object):
    vertical_walls: BoardBitmap
    horizontal_walls: BoardBitmap

    def __init__(self, vertical_walls: BoardBitmap, horizontal_walls: BoardBitmap) -> None:
        self.vertical_walls = vertical_walls
        self.horizontal_walls = horizontal_walls

    @classmethod
    def empty(cls):
        vertical_walls = BoardBitmap(VERTICAL_WALLS_START_STATE)
        horizontal_walls = BoardBitmap(HORIZONTAL_WALLS_START_STATE)

        return cls(vertical_walls, horizontal_walls)

    @classmethod
    def from_bigint(cls, serialized: int):
        """
        Serialization scheme as bigint:

        first 256 bits: vertical walls bitmap
        next 256 bits: horizontal walls bitmap
        """
        vertical_walls_val = serialized >> 256
        vertical_walls = BoardBitmap(vertical_walls_val)

        horizontal_walls_val = serialized & ((1 << 256) - 1)
        horizontal_walls = BoardBitmap(horizontal_walls_val)

        return cls(vertical_walls, horizontal_walls)



    def __int__(self) -> int:
        vertical_walls_val = self.vertical_walls.bitmap
        horizontal_walls_val = self.horizontal_walls.bitmap

        serialized = 0
        serialized |= self.vertical_walls.bitmap
        serialized = serialized << 256
        serialized |= self.horizontal_walls.bitmap
        serialized = serialized << 8

        serialized = vertical_walls_val << 256 | \
                horizontal_walls_val

        return serialized

    def __hash__(self) -> int:
        return int(self)
