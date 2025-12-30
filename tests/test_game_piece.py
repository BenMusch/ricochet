import pytest

from ricochet_solver.game_piece import EncodedPos

def test_encoded_pos():
    pos = EncodedPos.from_xy(3, 5)
    assert pos.x == 3
    assert pos.y == 5
    assert int(pos) == (5 << 4) | 3
