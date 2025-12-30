import pytest

from ricochet_solver.game_board import Board, BoardBitmap


def test_board_bitmap():
    positions = [(0, 0), (1, 2), (3, 3), (4, 4), (15, 15)]
    bitmap = BoardBitmap.from_positions(positions)
    
    for x, y in positions:
        assert bitmap.has(x, y)
    
    assert not bitmap.has(2, 2)
    assert not bitmap.has(4, 0)

    assert bitmap.row(0) == 0b0000000000000001
    assert bitmap.row(1) == 0b0000000000000000
    assert bitmap.row(2) == 0b0000000000000010
    assert bitmap.row(15) == 0b1000000000000000

    assert bitmap.scan_right_from(0, 0) == 0
    assert bitmap.scan_right_from(0, 2) == 1
    assert bitmap.scan_right_from(1, 2) == 1
    assert bitmap.scan_right_from(2, 2) == 15
    assert bitmap.scan_right_from(14, 15) == 15

    assert bitmap.scan_left_from(15, 15) == 0
    assert bitmap.scan_left_from(14, 0) == 1
    assert bitmap.scan_left_from(14, 3) == 4
    assert bitmap.scan_left_from(0, 0) == 0
    assert bitmap.scan_left_from(3, 3) == 0

    assert bitmap.column(0) == 0b0000000000000001
    assert bitmap.column(1) == 0b0000000000000100
    assert bitmap.column(2) == 0b0000000000000000
    assert bitmap.column(15) == 0b1000000000000000

    assert bitmap.scan_down_from(0, 0) == 0
    assert bitmap.scan_down_from(0, 1) == 15
    assert bitmap.scan_down_from(1, 0) == 2
    assert bitmap.scan_down_from(1, 2) == 2
    assert bitmap.scan_down_from(1, 3) == 15
    assert bitmap.scan_down_from(15, 14) == 15

    assert bitmap.scan_up_from(15, 15) == 0
    assert bitmap.scan_up_from(0, 14) == 1
    assert bitmap.scan_up_from(3, 14) == 4
    assert bitmap.scan_up_from(0, 0) == 0
    assert bitmap.scan_up_from(3, 3) == 0



def test_encoded_board_as_int():
    vertical_bitmap = BoardBitmap.from_positions(
        [(0, 0), (1, 2), (3, 3), (4, 4)]
    )
    horizontal_bitmap = BoardBitmap.from_positions(
        [(0, 1), (2, 2), (3, 0), (4, 3)]
    )
    board = Board(
        vertical_walls=vertical_bitmap,
        horizontal_walls=horizontal_bitmap,
    )

    board_int = int(board)
    parsed = Board.from_bigint(board_int)

    assert parsed.vertical_walls.has(0, 0)
    assert parsed.vertical_walls.has(1, 2)
    assert parsed.vertical_walls.bitmap == board.vertical_walls.bitmap
    assert parsed.horizontal_walls.bitmap == board.horizontal_walls.bitmap
