from ricochet_solver.game_board import Board
from ricochet_solver.game_piece import EncodedPos, PieceSet

from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def get_move_end(board: Board, pieces: PieceSet, start: EncodedPos, direction: Direction) -> EncodedPos:
    if direction == Direction.LEFT:
        return move_left(board, pieces, start)
    elif direction == Direction.RIGHT:
        return move_right(board, pieces, start)
    elif direction == Direction.UP:
        return move_up(board, pieces, start)
    elif direction == Direction.DOWN:
        return move_down(board, pieces, start)

def move_left(board: Board, pieces: PieceSet, start: EncodedPos) -> EncodedPos:
    leftmost_terminal = board.vertical_walls.scan_left_from(start.x, start.y)
    for piece in pieces:
        if piece.y == start.y and piece.x < start.x:
            leftmost_terminal = max(leftmost_terminal, piece.x + 1)

    return EncodedPos.from_xy(leftmost_terminal, start.y)

def move_right(board: Board, pieces: PieceSet, start: EncodedPos) -> EncodedPos:
    rightmost_terminal = board.vertical_walls.scan_right_from(start.x, start.y)
    for piece in pieces:
        if piece.y == start.y and piece.x > start.x:
            rightmost_terminal = min(rightmost_terminal, piece.x - 1)

    return EncodedPos.from_xy(rightmost_terminal, start.y)

def move_up(board: Board, pieces: PieceSet, start: EncodedPos) -> EncodedPos:
    topmost_terminal = board.horizontal_walls.scan_up_from(start.x, start.y)
    for piece in pieces:
        if piece.x == start.x and piece.y < start.y:
            topmost_terminal = max(topmost_terminal, piece.y + 1)

    return EncodedPos.from_xy(start.x, topmost_terminal)

def move_down(board: Board, pieces: PieceSet, start: EncodedPos) -> EncodedPos:
    bottommost_terminal = board.horizontal_walls.scan_down_from(start.x, start.y)
    for piece in pieces:
        if piece.x == start.x and piece.y > start.y:
            bottommost_terminal = min(bottommost_terminal, piece.y - 1)

    return EncodedPos.from_xy(start.x, bottommost_terminal)
