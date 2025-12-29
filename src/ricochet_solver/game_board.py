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


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


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


class EncodedPos:
    encoded: int

    def __init__(self, encoded: int) -> None:
        self.encoded = encoded

    @classmethod
    def from_xy(cls, x: int, y: int):
        return EncodedPos((y << 4) | x)

    @property
    def x(self) -> int:
        return self.encoded & 0b1111

    @property
    def y(self) -> int:
        return (self.encoded >> 4) & 0b1111

    def __int__(self) -> int:
        return self.encoded

    def __hash__(self) -> int:
        return self.encoded


class Target:
    color: Color
    position: EncodedPos

    def __init__(self, color: Color, position: EncodedPos) -> None:
        self.color = color
        self.position = position

    def __int__(self) -> int:
        return (self.color.value << 8) | self.position.encoded

class PieceSet:
    red: EncodedPos
    blue: EncodedPos
    green: EncodedPos
    yellow: EncodedPos

    def __init__(self, red: EncodedPos, blue: EncodedPos, green: EncodedPos,
                 yellow: EncodedPos) -> None:
        self.red = red
        self.blue = blue
        self.green = green
        self.yellow = yellow

    def get(self, color: Color) -> EncodedPos:
        if color == Color.RED:
            return self.red
        elif color == Color.BLUE:
            return self.blue
        elif color == Color.GREEN:
            return self.green
        elif color == Color.YELLOW:
            return self.yellow
        else:
            raise ValueError(f"Invalid color: {color}")

    def __int__(self) -> int:
        red_val = self.red.encoded
        blue_val = self.blue.encoded
        green_val = self.green.encoded
        yellow_val = self.yellow.encoded

        return red_val << 24 | \
            blue_val << 16 | \
            green_val << 8 | \
            yellow_val

    def __iter__(self):
        yield self.red
        yield self.blue
        yield self.green
        yield self.yellow

    def __hash__(self) -> int:
        return int(self)


class GameBoard(object):
    pieces: PieceSet
    target: Target
    vertical_walls: BoardBitmap
    horizontal_walls: BoardBitmap

    def __init__(self, vertical_walls: BoardBitmap, horizontal_walls:
                 BoardBitmap, pieces: PieceSet, target: Target) -> None:
        self.vertical_walls = vertical_walls
        self.horizontal_walls = horizontal_walls
        self.pieces = pieces
        self.target = target

    @classmethod
    def empty(cls):
        vertical_walls = BoardBitmap(VERTICAL_WALLS_START_STATE)
        horizontal_walls = BoardBitmap(HORIZONTAL_WALLS_START_STATE)

        target = Target(Color.RED, EncodedPos.from_xy(0, 0))
        pieces = PieceSet(
            EncodedPos.from_xy(1, 1),
            EncodedPos.from_xy(2, 2),
            EncodedPos.from_xy(3, 3),
            EncodedPos.from_xy(4, 4),
        )

        return cls(vertical_walls, horizontal_walls, pieces, target)

    @classmethod
    def from_bigint(cls, serialized: int):
        """
        Serialization scheme as bigint:

        first 256 bits: vertical walls bitmap
        next 256 bits: horizontal walls bitmap
        next 8 bits: red piece x,y
        next 8 bits: blue piece x,y
        next 8 bits: green piece x,y
        next 8 bits: yellow piece x,y
        next 8 bits: target piece x,y
        next 2 bits: target color encoded according to Color enum
        """
        # 298 = 256 (bits for horizontal walls) + 8*4 (bits for pieces) +
        # 8 (bits for target) + 2 (bits for target color)
        vertical_walls_val = serialized >> 298
        vertical_walls = BoardBitmap(vertical_walls_val)

        # 42 = 8*4 (bits for pieces) + 8 (bits for target) + 2 (bits for target color)
        horizontal_walls_val = (serialized >> 42) & ((1 << 256) - 1)
        horizontal_walls = BoardBitmap(horizontal_walls_val)

        red_piece_val = (serialized >> 34) & 0b11111111
        blue_piece_val = (serialized >> 26) & 0b11111111
        green_piece_val = (serialized >> 18) & 0b11111111
        yellow_piece_val = (serialized >> 10) & 0b11111111

        pieces = PieceSet(
            EncodedPos(red_piece_val),
            EncodedPos(blue_piece_val),
            EncodedPos(green_piece_val),
            EncodedPos(yellow_piece_val)
        )

        target_position_val = (serialized & 0b1111111100) >> 2
        target_color_val = serialized & 0b11

        target_position = EncodedPos(target_position_val)
        target_color = Color(target_color_val)
        target = Target(target_color, target_position)

        return cls(vertical_walls, horizontal_walls, pieces, target)

    def terminal_point_for_move(self, start: EncodedPos, direction: Direction) -> EncodedPos:
        if direction == Direction.LEFT:
            return self.move_left(start)
        elif direction == Direction.RIGHT:
            return self.move_right(start)
        elif direction == Direction.UP:
            return self.move_up(start)
        elif direction == Direction.DOWN:
            return self.move_down(start)

    def move_left(self, start) -> EncodedPos:
        leftmost_terminal = self.vertical_walls.scan_left_from(start.x, start.y)
        for piece in self.pieces:
            if piece.y == start.y and piece.x < start.x:
                leftmost_terminal = max(leftmost_terminal, piece.x + 1)

        return EncodedPos.from_xy(leftmost_terminal, start.y)

    def move_right(self, start) -> EncodedPos:
        rightmost_terminal = self.vertical_walls.scan_right_from(start.x, start.y)
        for piece in self.pieces:
            if piece.y == start.y and piece.x > start.x:
                rightmost_terminal = min(rightmost_terminal, piece.x - 1)

        return EncodedPos.from_xy(rightmost_terminal, start.y)

    def move_up(self, start) -> EncodedPos:
        topmost_terminal = self.horizontal_walls.scan_up_from(start.x, start.y)
        for piece in self.pieces:
            if piece.x == start.x and piece.y < start.y:
                topmost_terminal = max(topmost_terminal, piece.y + 1)

        return EncodedPos.from_xy(start.x, topmost_terminal)

    def move_down(self, start) -> EncodedPos:
        bottommost_terminal = self.horizontal_walls.scan_down_from(start.x, start.y)
        for piece in self.pieces:
            if piece.x == start.x and piece.y > start.y:
                bottommost_terminal = min(bottommost_terminal, piece.y - 1)

        return EncodedPos.from_xy(start.x, bottommost_terminal)

    def is_solved(self):
        return self.pieces.get(self.target.color).encoded == self.target.position.encoded


    def __int__(self) -> int:
        vertical_walls_val = self.vertical_walls.bitmap
        horizontal_walls_val = self.horizontal_walls.bitmap

        serialized = 0
        serialized |= self.vertical_walls.bitmap
        serialized = serialized << 256
        serialized |= self.horizontal_walls.bitmap
        serialized = serialized << 8

        target_val = self.target.position.encoded
        target_color_val = self.target.color.value

        serialized = vertical_walls_val << 298 | \
                horizontal_walls_val << 42 | \
                int(self.pieces) << 10 | \
                target_val << 2 | \
                target_color_val

        return serialized

    def __hash__(self) -> int:
        return int(self)
