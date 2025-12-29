import pytest

from ricochet_solver.game_board import BoardBitmap, Target, EncodedPos, \
    Color, GameBoard, Direction, PieceSet


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



def test_encoded_pos():
    pos = EncodedPos.from_xy(3, 5)
    assert pos.x == 3
    assert pos.y == 5
    assert int(pos) == (5 << 4) | 3


def test_encoded_board_as_int():
    vertical_bitmap = BoardBitmap.from_positions(
        [(0, 0), (1, 2), (3, 3), (4, 4)]
    )
    horizontal_bitmap = BoardBitmap.from_positions(
        [(0, 1), (2, 2), (3, 0), (4, 3)]
    )
    pieces = PieceSet(
        EncodedPos.from_xy(1, 1),
        EncodedPos.from_xy(2, 3),
        EncodedPos.from_xy(3, 4),
        EncodedPos.from_xy(4, 0)
    )
    target = Target(
        color=Color.YELLOW,
        position=EncodedPos.from_xy(15, 13)
    )
    board = GameBoard(
        vertical_walls=vertical_bitmap,
        horizontal_walls=horizontal_bitmap,
        pieces=pieces,
        target=target
    )

    board_int = int(board)
    parsed = GameBoard.from_bigint(board_int)

    assert parsed.vertical_walls.has(0, 0)
    assert parsed.vertical_walls.has(1, 2)
    assert parsed.vertical_walls.bitmap == board.vertical_walls.bitmap
    assert parsed.horizontal_walls.bitmap == board.horizontal_walls.bitmap
    assert parsed.pieces.red.encoded == board.pieces.red.encoded
    assert parsed.pieces.blue.encoded == board.pieces.blue.encoded
    assert parsed.pieces.green.encoded == board.pieces.green.encoded
    assert parsed.pieces.yellow.encoded == board.pieces.yellow.encoded

    assert parsed.target.color == board.target.color
    assert parsed.target.position.encoded == board.target.position.encoded

def test_move_left_stops_at_edge():
    board = GameBoard(
        vertical_walls=BoardBitmap(0),
        horizontal_walls=BoardBitmap(0),
        pieces=PieceSet(
            EncodedPos.from_xy(5, 5),
            EncodedPos.from_xy(10, 10),
            EncodedPos.from_xy(15, 15),
            EncodedPos.from_xy(0, 0),
        ),
        target=Target(Color.RED, EncodedPos.from_xy(0, 0))
    )

    terminal_pos = board.terminal_point_for_move(
        start=EncodedPos.from_xy(3, 3),
        direction=Direction.LEFT,
    )
    assert terminal_pos.x == 0
    assert terminal_pos.y == 3

def test_move_left_stops_at_wall():
    board = GameBoard(
        vertical_walls=BoardBitmap.from_positions(
            [(2, 3), (1, 3), (3, 4), (7, 3)]
        ),
        horizontal_walls=BoardBitmap(0),
        pieces=PieceSet(
            EncodedPos.from_xy(5, 5),
            EncodedPos.from_xy(10, 10),
            EncodedPos.from_xy(15, 15),
            EncodedPos.from_xy(0, 0),
        ),
        target=Target(Color.RED, EncodedPos.from_xy(0, 0))
    )

    terminal_pos = board.terminal_point_for_move(
        start=EncodedPos.from_xy(4, 3),
        direction=Direction.LEFT,
    )

    assert terminal_pos.x == 3
    assert terminal_pos.y == 3

def test_move_left_stops_at_piece():
    board = GameBoard(
        vertical_walls=BoardBitmap.from_positions(
            [(2, 3), (7, 3)]
        ),
        horizontal_walls=BoardBitmap(0),
        pieces=PieceSet(
            EncodedPos.from_xy(5, 5),
            EncodedPos.from_xy(3, 3),
            EncodedPos.from_xy(15, 15),
            EncodedPos.from_xy(0, 0)
        ),
        target=Target(Color.RED, EncodedPos.from_xy(0, 3))
    )

    terminal_pos = board.terminal_point_for_move(
        start=EncodedPos.from_xy(5, 3),
        direction=Direction.LEFT,
    )

    assert terminal_pos.x == 4
    assert terminal_pos.y == 3
