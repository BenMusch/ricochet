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

def test_move_right_stops_at_edge():
    board = Board(
        vertical_walls=BoardBitmap(0),
        horizontal_walls=BoardBitmap(0),
    )

    pieces = PieceSet(
        EncodedPos.from_xy(5, 5),
        EncodedPos.from_xy(10, 10),
        EncodedPos.from_xy(0, 0),
        EncodedPos.from_xy(1, 1),
    )

    terminal_pos = get_move_end(
        board,
        pieces,
        EncodedPos.from_xy(3, 3),
        Direction.RIGHT,
    )
    assert terminal_pos.x == 15
    assert terminal_pos.y == 3

def test_move_right_stops_at_wall():
    board = Board(
        vertical_walls=BoardBitmap.from_positions(
            [(5, 3), (8, 3), (3, 4)]
        ),
        horizontal_walls=BoardBitmap(0),
    )

    pieces = PieceSet(
        EncodedPos.from_xy(0, 0),
        EncodedPos.from_xy(10, 10),
        EncodedPos.from_xy(15, 15),
        EncodedPos.from_xy(1, 1),
    )

    terminal_pos = get_move_end(
        board,
        pieces,
        EncodedPos.from_xy(3, 3),
        Direction.RIGHT,
    )

    assert terminal_pos.x == 5
    assert terminal_pos.y == 3

def test_move_right_stops_at_piece():
    board = Board(
        vertical_walls=BoardBitmap(0),
        horizontal_walls=BoardBitmap(0),
    )

    pieces = PieceSet(
        EncodedPos.from_xy(5, 5),
        EncodedPos.from_xy(8, 3),
        EncodedPos.from_xy(15, 15),
        EncodedPos.from_xy(0, 0),
    )

    terminal_pos = get_move_end(
        board,
        pieces,
        EncodedPos.from_xy(3, 3),
        Direction.RIGHT,
    )

    assert terminal_pos.x == 7
    assert terminal_pos.y == 3

def test_move_up_stops_at_edge():
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
        Direction.UP,
    )
    assert terminal_pos.x == 3
    assert terminal_pos.y == 0

def test_move_up_stops_at_wall():
    board = Board(
        vertical_walls=BoardBitmap(0),
        horizontal_walls=BoardBitmap.from_positions(
            [(3, 2), (3, 1), (4, 3), (3, 7)]
        ),
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
        EncodedPos.from_xy(3, 4),
        Direction.UP,
    )

    assert terminal_pos.x == 3
    assert terminal_pos.y == 3

def test_move_up_stops_at_piece():
    board = Board(
        vertical_walls=BoardBitmap(0),
        horizontal_walls=BoardBitmap(0),
    )

    pieces = PieceSet(
        EncodedPos.from_xy(5, 5),
        EncodedPos.from_xy(3, 3),
        EncodedPos.from_xy(15, 15),
        EncodedPos.from_xy(0, 0),
    )

    terminal_pos = get_move_end(
        board,
        pieces,
        EncodedPos.from_xy(3, 5),
        Direction.UP,
    )

    assert terminal_pos.x == 3
    assert terminal_pos.y == 4

def test_move_down_stops_at_edge():
    board = Board(
        vertical_walls=BoardBitmap(0),
        horizontal_walls=BoardBitmap(0),
    )

    pieces = PieceSet(
        EncodedPos.from_xy(5, 5),
        EncodedPos.from_xy(10, 10),
        EncodedPos.from_xy(0, 0),
        EncodedPos.from_xy(1, 1),
    )

    terminal_pos = get_move_end(
        board,
        pieces,
        EncodedPos.from_xy(3, 3),
        Direction.DOWN,
    )
    assert terminal_pos.x == 3
    assert terminal_pos.y == 15

def test_move_down_stops_at_wall():
    board = Board(
        vertical_walls=BoardBitmap(0),
        horizontal_walls=BoardBitmap.from_positions(
            [(3, 5), (3, 8), (4, 3)]
        ),
    )

    pieces = PieceSet(
        EncodedPos.from_xy(0, 0),
        EncodedPos.from_xy(10, 10),
        EncodedPos.from_xy(15, 15),
        EncodedPos.from_xy(1, 1),
    )

    terminal_pos = get_move_end(
        board,
        pieces,
        EncodedPos.from_xy(3, 3),
        Direction.DOWN,
    )

    assert terminal_pos.x == 3
    assert terminal_pos.y == 5

def test_move_down_stops_at_piece():
    board = Board(
        vertical_walls=BoardBitmap(0),
        horizontal_walls=BoardBitmap(0),
    )

    pieces = PieceSet(
        EncodedPos.from_xy(5, 5),
        EncodedPos.from_xy(3, 8),
        EncodedPos.from_xy(15, 15),
        EncodedPos.from_xy(0, 0),
    )

    terminal_pos = get_move_end(
        board,
        pieces,
        EncodedPos.from_xy(3, 3),
        Direction.DOWN,
    )

    assert terminal_pos.x == 3
    assert terminal_pos.y == 7