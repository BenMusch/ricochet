import pytest

from ricochet_solver.game_board import GameBoard

def test_add_wall_out_of_bounds():
    board = GameBoard()

    with pytest.raises(AssertionError):
        board.add_vertical_wall(15, 3) 
    board.add_vertical_wall(14, 3) 

    with pytest.raises(AssertionError):
        board.add_vertical_wall(-1, 3)
    board.add_vertical_wall(0, 3)

    with pytest.raises(AssertionError):
        board.add_horizontal_wall(5, 15)
    board.add_horizontal_wall(5, 14)

    with pytest.raises(AssertionError):
        board.add_horizontal_wall(5, -1)
    board.add_horizontal_wall(5, 0)

def test_adding_vertical_walls() -> None:
    board = GameBoard()

    assert not board.has_vertical_wall(5, 5)
    board.add_vertical_wall(5, 5)

    assert board.has_vertical_wall(5, 5)
    board.remove_vertical_wall(5, 5)

    assert not board.has_vertical_wall(5, 5)

def test_adding_horizontal_walls() -> None:
    board = GameBoard()
    assert not board.has_horizontal_wall(7, 8)

    board.add_horizontal_wall(7, 8)
    assert board.has_horizontal_wall(7, 8)

    board.remove_horizontal_wall(7, 8)
    assert not board.has_horizontal_wall(7, 8)

def test_adding_horizontal_and_vertical_walls() -> None:
    board = GameBoard()

    assert not board.has_horizontal_wall(4, 4)
    assert not board.has_vertical_wall(4, 4)

    board.add_horizontal_wall(4, 4)

    assert board.has_horizontal_wall(4, 4)
    assert not board.has_vertical_wall(4, 4)

    board.add_vertical_wall(4, 4)

    assert board.has_horizontal_wall(4, 4)
    assert board.has_vertical_wall(4, 4)

    board.remove_horizontal_wall(4, 4)

    assert not board.has_horizontal_wall(4, 4)
    assert board.has_vertical_wall(4, 4)
