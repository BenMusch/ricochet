"""Flask web app for ricochet-solver."""

from flask import Flask, jsonify, render_template, request

from ricochet_solver.game_board import (
    GRID_SIZE,
    HORIZONTAL_WALLS_START_STATE,
    VERTICAL_WALLS_START_STATE,
)

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the main page."""
    return render_template("index.html")


@app.route("/api/validate", methods=["POST"])
def validate_board():
    """Validate a board state.

    Expects JSON with:
        - verticalWalls: string representation of the vertical walls bitmask
        - horizontalWalls: string representation of the horizontal walls bitmask

    Returns:
        - valid: boolean indicating if the board state is valid
        - errors: list of validation error messages
    """
    data = request.json
    errors = []

    try:
        vertical_walls = int(data.get("verticalWalls", "0"))
        horizontal_walls = int(data.get("horizontalWalls", "0"))
    except (ValueError, TypeError):
        return jsonify({"valid": False, "errors": ["Invalid wall data format"]})

    max_bits = (GRID_SIZE - 1) * (GRID_SIZE - 1)
    max_value = (1 << max_bits) - 1

    if vertical_walls < 0 or vertical_walls > max_value:
        errors.append("Vertical walls value out of range")

    if horizontal_walls < 0 or horizontal_walls > max_value:
        errors.append("Horizontal walls value out of range")

    if (vertical_walls & VERTICAL_WALLS_START_STATE) != VERTICAL_WALLS_START_STATE:
        errors.append("Center vertical walls have been modified")

    if (horizontal_walls & HORIZONTAL_WALLS_START_STATE) != HORIZONTAL_WALLS_START_STATE:
        errors.append("Center horizontal walls have been modified")

    return jsonify({
        "valid": len(errors) == 0,
        "errors": errors
    })


@app.route("/api/initial-state")
def get_initial_state():
    """Get the initial board state constants."""
    return jsonify({
        "gridSize": GRID_SIZE,
        "verticalWalls": str(VERTICAL_WALLS_START_STATE),
        "horizontalWalls": str(HORIZONTAL_WALLS_START_STATE)
    })


def run():
    """Run the web server."""
    app.run(debug=True, port=8000)
