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
        bitmap = cls(0)
        for x, y in positions:
            bitmap.set(x, y)

    def is_set(self, x: int, y: int) -> bool:
        index = y * (GRID_SIZE - 1) + x
        return (self.bitmap & (1 << index)) != 0

    def set(self, x: int, y: int) -> None:
        index = y * (GRID_SIZE - 1) + x
        self.bitmap |= (1 << index)

    def clear(self, x: int, y: int) -> None:
        index = y * (GRID_SIZE - 1) + x
        self.bitmap &= ~(1 << index)

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
        vertical_walls = BoardBitmap(serialized & (1 << 256 - 1))
        serialized = serialized >> 256
        horizontal_walls = BoardBitmap(serialized & (1 << 256 - 1))
        serialized = serialized >> 256

        red_piece = ColoredPiece(
            Color.RED,
            EncodedPos(serialized & 0b11111111)
        )
        serialized = serialized >> 8
        blue_piece = ColoredPiece(
            Color.BLUE,
            EncodedPos(serialized & 0b11111111)
        )
        serialized = serialized >> 8
        green_piece = ColoredPiece(
            Color.GREEN,
            EncodedPos(serialized & 0b11111111)
        )
        serialized = serialized >> 8
        yellow_piece = ColoredPiece(
            Color.YELLOW,
            EncodedPos(serialized & 0b11111111)
        )
        serialized = serialized >> 8
        pieces = [red_piece, blue_piece, green_piece, yellow_piece]

        target_position = EncodedPos(serialized & 0b11111111)
        serialized = serialized >> 8
        target_color = Color(serialized & 0b11)
        target = ColoredPiece(target_color, target_position)

        return cls(vertical_walls, horizontal_walls, pieces, target)

    def __int__(self) -> int:
        serialized = 0
        serialized |= self.vertical_walls.bitmap
        serialized = serialized << 256
        serialized |= self.horizontal_walls.bitmap
        serialized = serialized << 8

        color_order = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
        for color in color_order:
            piece = next(p for p in self.pieces if p.color == color)
            serialized |= piece.position.encoded
            serialized = serialized << 8

        serialized |= self.target.position.encoded
        serialized = serialized << 2
        serialized |= self.target.color.value

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
