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

class BoardBitmap:
    bitmap: int

    def __init__(self, bitmap: int) -> None:
        self.bitmap = bitmap

    @classmethod
    def from_positions(cls, positions: list[tuple[int, int]]):
        bitmap = 0
        for x, y in positions:
            bitmap |= (1 << (y * (GRID_SIZE - 1) + x))
        return cls(bitmap)

    def has(self, x: int, y: int) -> bool:
        index = y * (GRID_SIZE - 1) + x
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


class ColoredPiece:
    color: Color
    position: EncodedPos

    def __init__(self, color: Color, position: EncodedPos) -> None:
        self.color = color
        self.position = position

    def __int__(self) -> int:
        return (self.color.value << 8) | self.position.encoded


class GameBoard(object):
    pieces: list[ColoredPiece]
    target: ColoredPiece
    vertical_walls: BoardBitmap
    horizontal_walls: BoardBitmap

    def __init__(self, vertical_walls: BoardBitmap, horizontal_walls: BoardBitmap, pieces: list[ColoredPiece], target: ColoredPiece) -> None:
        self.vertical_walls = vertical_walls
        self.horizontal_walls = horizontal_walls
        self.pieces = pieces
        self.target = target

    @classmethod
    def empty(cls):
        vertical_walls = BoardBitmap(VERTICAL_WALLS_START_STATE)
        horizontal_walls = BoardBitmap(HORIZONTAL_WALLS_START_STATE)

        target = ColoredPiece(Color.RED, EncodedPos.from_xy(0, 0))
        pieces = [
            ColoredPiece(Color.RED, EncodedPos.from_xy(1, 1)),
            ColoredPiece(Color.BLUE, EncodedPos.from_xy(2, 2)),
            ColoredPiece(Color.GREEN, EncodedPos.from_xy(3, 3)),
            ColoredPiece(Color.YELLOW, EncodedPos.from_xy(4, 4)),
        ]

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

        red_piece = ColoredPiece(
            Color.RED,
            EncodedPos(red_piece_val)
        )
        blue_piece = ColoredPiece(
            Color.BLUE,
            EncodedPos(blue_piece_val)
        )
        green_piece = ColoredPiece(
            Color.GREEN,
            EncodedPos(green_piece_val)
        )
        yellow_piece = ColoredPiece(
            Color.YELLOW,
            EncodedPos(yellow_piece_val)
        )

        pieces = [red_piece, blue_piece, green_piece, yellow_piece]

        target_position_val = (serialized & 0b1111111100) >> 2
        target_color_val = serialized & 0b11

        target_position = EncodedPos(target_position_val)
        target_color = Color(target_color_val)
        target = ColoredPiece(target_color, target_position)

        return cls(vertical_walls, horizontal_walls, pieces, target)

    def __int__(self) -> int:
        vertical_walls_val = self.vertical_walls.bitmap
        horizontal_walls_val = self.horizontal_walls.bitmap

        serialized = 0
        serialized |= self.vertical_walls.bitmap
        serialized = serialized << 256
        serialized |= self.horizontal_walls.bitmap
        serialized = serialized << 8

        sorted_pieces = sorted(self.pieces, key=lambda p: p.color.value)
        [red_piece, blue_piece, green_piece, yellow_piece] = sorted_pieces

        red_val = red_piece.position.encoded
        blue_val = blue_piece.position.encoded
        green_val = green_piece.position.encoded
        yellow_val = yellow_piece.position.encoded

        target_val = self.target.position.encoded
        target_color_val = self.target.color.value

        serialized = vertical_walls_val << 298 | \
                horizontal_walls_val << 42 | \
                red_val << 34 | \
                blue_val << 26 | \
                green_val << 18 | \
                yellow_val << 10 | \
                target_val << 2 | \
                target_color_val

        return serialized

    def __hash__(self) -> int:
        return int(self)

    def throw_if_invalid(self) -> None:
        assert len(self.pieces) == 4, "There must be exactly 4 pieces on the board."
        assert len(set(piece.color for piece in self.pieces)) == 4, "Each piece must have a unique color."

        all_positions = set()
        all_positions.add(self.target.position.encoded)

        for piece in self.pieces:
            assert piece.position.encoded not in all_positions, "No two pieces can occupy the same position."
            all_positions.add(piece.position.encoded)
