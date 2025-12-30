from typing import TypeAlias
from enum import Enum
from collections import deque
import heapq

from ricochet_solver.game_board import Board
from ricochet_solver.game_piece import EncodedPos, PieceSet, Color, Target

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

Move: TypeAlias = tuple[Color, Direction]


def find_solution(board: Board, pieces: PieceSet, target: Target):
    """Find solution using A* with minimum-turns heuristic."""

    # Precompute minimum turns from every reachable position to the target
    min_turns_to_goal = _precompute_min_turns(board, target.position)

    def heuristic(piece_pos: EncodedPos) -> int:
        return min_turns_to_goal.get(piece_pos.encoded, 1000)

    # Check if already solved
    if pieces.get(target.color) == target.position:
        return []

    initial_key = int(pieces)
    initial_h = heuristic(pieces.get(target.color))

    # Priority queue: (f_score, tie_breaker, g_score, pieces_key, pieces, moves)
    # tie_breaker ensures consistent ordering when f_scores are equal
    counter = 0
    heap = [(initial_h, counter, 0, initial_key, pieces, [])]

    # Track best g_score for each state
    best_g: dict[int, int] = {initial_key: 0}

    while heap:
        f, _, g, cur_key, cur_pieces, cur_moves = heapq.heappop(heap)

        # Skip if we've found a better path to this state
        if g > best_g.get(cur_key, float('inf')):
            continue

        if g > 30:
            continue

        for move in generate_moves():
            new_pieces = apply_move(board, cur_pieces, move)

            # Skip no-op moves (piece didn't move)
            if new_pieces.get(move[0]) == cur_pieces.get(move[0]):
                continue

            # Check for solution
            if move[0] == target.color and new_pieces.get(move[0]) == target.position:
                return cur_moves + [move]

            new_key = int(new_pieces)
            new_g = g + 1

            # Skip if we've seen this state with equal or better cost
            if new_g >= best_g.get(new_key, float('inf')):
                continue

            best_g[new_key] = new_g
            new_h = heuristic(new_pieces.get(target.color))
            new_f = new_g + new_h

            counter += 1
            heapq.heappush(heap, (new_f, counter, new_g, new_key, new_pieces, cur_moves + [move]))

    raise ValueError("No solution found")


def _precompute_min_turns(board: Board, goal: EncodedPos) -> dict[int, int]:
    """
    Precompute minimum turns from every position to the goal, ignoring other pieces.
    Uses reverse BFS: starting from goal, find all positions that can reach it.
    """
    min_turns: dict[int, int] = {goal.encoded: 0}

    # For reverse search, we need to find positions that can slide TO a given position
    # A piece at position P can slide to position Q if:
    # - They're on the same row/column
    # - Q is at a wall boundary in that direction
    # - There are no walls between P and Q that would stop P before reaching Q

    # Simpler approach: BFS from every position, cache results
    # But more efficient: work backwards from goal

    # For each position in min_turns, find all positions that can reach it in one move
    queue = deque([goal])

    while queue:
        pos = queue.popleft()
        current_turns = min_turns[pos.encoded]

        # Find all positions that can slide to 'pos' in one move
        for source in _positions_that_slide_to(board, pos):
            if source.encoded not in min_turns:
                min_turns[source.encoded] = current_turns + 1
                queue.append(source)

    return min_turns


def _positions_that_slide_to(board: Board, target_pos: EncodedPos):
    """
    Yield all positions that, when sliding in some direction, would stop at target_pos.
    A piece stops at target_pos if target_pos is at a wall/edge boundary.
    """
    x, y = target_pos.x, target_pos.y

    # Check if target_pos is a valid stopping point from the LEFT (piece sliding right)
    # Piece stops here if there's a vertical wall to the right, or it's the right edge
    if x == 15 or board.vertical_walls.has(x, y):
        # Any position to the left in this row (that isn't blocked) can slide here
        for src_x in range(x - 1, -1, -1):
            # Check if there's a wall between src_x and x
            if board.vertical_walls.has(src_x, y):
                break  # Wall blocks further sources
            yield EncodedPos.from_xy(src_x, y)

    # Check if target_pos is a valid stopping point from the RIGHT (piece sliding left)
    if x == 0 or board.vertical_walls.has(x - 1, y):
        for src_x in range(x + 1, 16):
            if src_x > 0 and board.vertical_walls.has(src_x - 1, y):
                break
            yield EncodedPos.from_xy(src_x, y)

    # Check if target_pos is a valid stopping point from ABOVE (piece sliding down)
    if y == 15 or board.horizontal_walls.has(x, y):
        for src_y in range(y - 1, -1, -1):
            if board.horizontal_walls.has(x, src_y):
                break
            yield EncodedPos.from_xy(x, src_y)

    # Check if target_pos is a valid stopping point from BELOW (piece sliding up)
    if y == 0 or board.horizontal_walls.has(x, y - 1):
        for src_y in range(y + 1, 16):
            if src_y > 0 and board.horizontal_walls.has(x, src_y - 1):
                break
            yield EncodedPos.from_xy(x, src_y)

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
        black=pieces.black,
    )

    if color == Color.RED:
        new_pieces.red = end_pos
    elif color == Color.BLUE:
        new_pieces.blue = end_pos
    elif color == Color.GREEN:
        new_pieces.green = end_pos
    elif color == Color.YELLOW:
        new_pieces.yellow = end_pos
    elif color == Color.BLACK:
        new_pieces.black = end_pos

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
