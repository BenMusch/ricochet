from typing import TypeAlias
from enum import Enum

from ricochet_solver.game_board import Board
from ricochet_solver.game_piece import EncodedPos, PieceSet, Color, Target

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

Move: TypeAlias = tuple[Color, Direction]


def find_solution(board: Board, pieces: PieceSet, target: Target):
    seen_positions = set()

    horizon: list[tuple[PieceSet, list[Move]]] = [
        (pieces, [])
    ]

    while horizon:
        cur_pieces, cur_moves = horizon.pop(0)

        if (len(cur_moves) > 30):
            raise ValueError("No solution found within 30 moves")

        for move in generate_moves():
            new_pieces = apply_move(board, cur_pieces, move)

            if int(new_pieces) in seen_positions:
                continue

            # solution will only be found when moving the target piece, only
            # bother check then
            if move[0] == target.color and new_pieces.get(move[0]) == target.position:
                return cur_moves + [move]

            seen_positions.add(int(new_pieces))

            new_moves = cur_moves + [move]
            horizon.append((new_pieces, new_moves))

    raise ValueError("No solution found")

def generate_moves():
    for direction in Direction:
        for color in Color:
            yield (color, direction)

def apply_move(board: Board, pieces: PieceSet, move: Move) -> PieceSet:
    color, direction = move
    start_pos = pieces.get(color)
    end_pos = get_move_end(board, pieces, start_pos, direction)

    new_pieces = PieceSet(
        red=pieces.red,
        blue=pieces.blue,
        green=pieces.green,
        yellow=pieces.yellow,
    )

    if color == Color.RED:
        new_pieces.red = end_pos
    elif color == Color.BLUE:
        new_pieces.blue = end_pos
    elif color == Color.GREEN:
        new_pieces.green = end_pos
    elif color == Color.YELLOW:
        new_pieces.yellow = end_pos

    return new_pieces


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
