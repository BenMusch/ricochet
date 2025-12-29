import pytest

from ricochet_solver.game_board import BoardBitmap, ColoredPiece, EncodedPos, \
    Color, GameBoard


def test_board_bitmap():
    positions = [(0, 0), (1, 2), (3, 3), (4, 4)]
    bitmap = BoardBitmap.from_positions(positions)
    
    for x, y in positions:
        assert bitmap.has(x, y)
    
    assert not bitmap.has(2, 2)
    assert not bitmap.has(4, 0)


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
    pieces = [
        ColoredPiece(color=Color.RED, position=EncodedPos.from_xy(1, 1)),
        ColoredPiece(color=Color.BLUE, position=EncodedPos.from_xy(2, 3)),
        ColoredPiece(color=Color.GREEN, position=EncodedPos.from_xy(3, 4)),
        ColoredPiece(color=Color.YELLOW, position=EncodedPos.from_xy(4, 0)),
    ]
    target = ColoredPiece(
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
    assert all(
        int(p1) == int(p2)
        for p1, p2 in zip(
            sorted(parsed.pieces, key=lambda p: p.color.value),
            sorted(board.pieces, key=lambda p: p.color.value),
        )
    )

    assert parsed.target.color == board.target.color
    assert parsed.target.position.encoded == board.target.position.encoded
