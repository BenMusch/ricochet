import pytest

from ricochet_solver.game_board import Board, BoardBitmap
from ricochet_solver.game_piece import EncodedPos, PieceSet
from ricochet_solver.movegen import get_move_end, Direction

def test_move_left_stops_at_edge():
    board = Board(
        vertical_walls=BoardBitmap(0),
        horizontal_walls=BoardBitmap(0),
    )

    pieces = PieceSet(
        EncodedPos.from_xy(5, 5),
        EncodedPos.from_xy(10, 10),
        EncodedPos.from_xy(15, 15),
        EncodedPos.from_xy(0, 0),
    )

    terminal_pos = get_move_end(
        board,
        pieces,
        EncodedPos.from_xy(3, 3),
        Direction.LEFT,
    )
    assert terminal_pos.x == 0
    assert terminal_pos.y == 3

def test_move_left_stops_at_wall():
    board = Board(
        vertical_walls=BoardBitmap.from_positions(
            [(2, 3), (1, 3), (3, 4), (7, 3)]
        ),
        horizontal_walls=BoardBitmap(0),
    )

    pieces = PieceSet(
        EncodedPos.from_xy(5, 5),
        EncodedPos.from_xy(10, 10),
        EncodedPos.from_xy(15, 15),
        EncodedPos.from_xy(0, 0),
    )

    terminal_pos = get_move_end(
        board,
        pieces,
        EncodedPos.from_xy(4, 3),
        Direction.LEFT,
    )

    assert terminal_pos.x == 3
    assert terminal_pos.y == 3

def test_move_left_stops_at_piece():
    board = Board(
        vertical_walls=BoardBitmap.from_positions(
            [(2, 3), (7, 3)]
        ),
        horizontal_walls=BoardBitmap(0),
    )

    pieces = PieceSet(
        EncodedPos.from_xy(5, 5),
        EncodedPos.from_xy(3, 3),
        EncodedPos.from_xy(15, 15),
        EncodedPos.from_xy(0, 0)
    )

    terminal_pos = get_move_end(
        board,
        pieces,
        EncodedPos.from_xy(5, 3),
        Direction.LEFT,
    )

    assert terminal_pos.x == 4
    assert terminal_pos.y == 3
