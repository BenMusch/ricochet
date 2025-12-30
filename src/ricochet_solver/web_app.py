"""Flask web app for ricochet-solver."""

from flask import Flask, jsonify, render_template, request

from ricochet_solver.game_board import (
    GRID_SIZE,
    HORIZONTAL_WALLS_START_STATE,
    VERTICAL_WALLS_START_STATE,
    Board,
    BoardBitmap,
)
from ricochet_solver.game_piece import Color, EncodedPos, PieceSet, Target
from ricochet_solver.movegen import find_solution

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the main page."""
    return render_template("index.html")


@app.route("/api/solve", methods=["POST"])
def solve():
    """Solve the puzzle and return the moves."""
    data = request.get_json()

    vertical_walls = int(data["vertical_walls"])
    horizontal_walls = int(data["horizontal_walls"])
    pieces_encoded = int(data["pieces"])
    target_pos = int(data["target"])
    target_color_idx = int(data["target_color"])

    board = Board(
        vertical_walls=BoardBitmap(vertical_walls),
        horizontal_walls=BoardBitmap(horizontal_walls),
    )

    red_pos = EncodedPos(pieces_encoded & 0xFF)
    blue_pos = EncodedPos((pieces_encoded >> 8) & 0xFF)
    green_pos = EncodedPos((pieces_encoded >> 16) & 0xFF)
    yellow_pos = EncodedPos((pieces_encoded >> 24) & 0xFF)
    black_pos = EncodedPos((pieces_encoded >> 32) & 0xFF)

    pieces = PieceSet(
        red=red_pos,
        blue=blue_pos,
        green=green_pos,
        yellow=yellow_pos,
        black=black_pos,
    )

    target_color = Color(target_color_idx)
    target = Target(color=target_color, position=EncodedPos(target_pos))

    try:
        solution = find_solution(board, pieces, target)
        moves = [
            {"color": move[0].name.lower(), "direction": move[1].name.lower()}
            for move in solution
        ]
        return jsonify({"success": True, "moves": moves})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)})


def run():
    """Run the web server."""
    app.run(debug=True, port=8000)
