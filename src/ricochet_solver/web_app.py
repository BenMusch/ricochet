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


def run():
    """Run the web server."""
    app.run(debug=True, port=8000)
