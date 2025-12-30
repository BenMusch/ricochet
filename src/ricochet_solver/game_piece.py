from enum import Enum

class Color(Enum):
    RED = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3
    BLACK = 4


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

    def __repr__(self) -> str:
        return f"EncodedPos(x={self.x}, y={self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EncodedPos):
            return False
        return self.encoded == other.encoded

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
    black: EncodedPos

    def __init__(self, red: EncodedPos, blue: EncodedPos, green: EncodedPos,
                 yellow: EncodedPos, black: EncodedPos) -> None:
        self.red = red
        self.blue = blue
        self.green = green
        self.yellow = yellow
        self.black = black

    def get(self, color: Color) -> EncodedPos:
        if color == Color.RED:
            return self.red
        elif color == Color.BLUE:
            return self.blue
        elif color == Color.GREEN:
            return self.green
        elif color == Color.YELLOW:
            return self.yellow
        elif color == Color.BLACK:
            return self.black
        else:
            raise ValueError(f"Invalid color: {color}")

    def __int__(self) -> int:
        red_val = self.red.encoded
        blue_val = self.blue.encoded
        green_val = self.green.encoded
        yellow_val = self.yellow.encoded
        black_val = self.black.encoded

        return red_val << 32 | \
            blue_val << 24 | \
            green_val << 16 | \
            yellow_val << 8 | \
            black_val

    def __iter__(self):
        yield self.red
        yield self.blue
        yield self.green
        yield self.yellow
        yield self.black

    def __hash__(self) -> int:
        return int(self)
