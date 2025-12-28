"""Textual app for ricochet-solver."""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header, Static

from ricochet_solver import game_board as gb


class GameBoard(Static):
    """A game board widget."""

    def __init__(self) -> None:
        super().__init__()
        self.cursor_x = 0
        self.cursor_y = 0
        self.board_size = 16
        self.board = gb.GameBoard()

    def on_mount(self) -> None:
        """Set up the board when mounted."""
        self.update_board()

    def update_board(self) -> None:
        """Render the game board."""
        lines = []
        for y in range(self.board_size):
            row = []
            for x in range(self.board_size):
                if x == self.cursor_x and y == self.cursor_y:
                    row.append("[bold yellow on blue]●[/]")
                elif (x + y) % 2 == 0:
                    row.append("[dim]·[/]")
                else:
                    row.append("[dim white]·[/]")

                if x < self.board_size - 1:
                    if y < self.board_size - 1 and self.board.has_vertical_wall(x, y):
                        row.append("[bold cyan]│[/] ")
                    else:
                        row.append("  ")

            lines.append("".join(row))

            if y < self.board_size - 1:
                wall_row = []
                for x in range(self.board_size - 1):
                    if self.board.has_horizontal_wall(x, y):
                        wall_row.append("[bold cyan]─[/] ")
                    else:
                        wall_row.append("  ")

                wall_row.append(" ")
                lines.append("".join(wall_row))

        self.update("\n".join(lines))


class RicochetSolverApp(App):
    """A Textual app for ricochet solver."""

    CSS = """
    GameBoard {
        width: 100%;
        height: 100%;
        content-align: center middle;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("up", "move_up", "Move Up"),
        ("down", "move_down", "Move Down"),
        ("left", "move_left", "Move Left"),
        ("right", "move_right", "Move Right"),
        ("w,a", "toggle_wall_above", "Wall Above"),
        ("w,b", "toggle_wall_below", "Wall Below"),
        ("w,l", "toggle_wall_left", "Wall Left"),
        ("w,r", "toggle_wall_right", "Wall Right"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(GameBoard())
        yield Footer()

    def action_move_up(self) -> None:
        """Move cursor up."""
        board = self.query_one(GameBoard)
        board.cursor_y = max(0, board.cursor_y - 1)
        board.update_board()

    def action_move_down(self) -> None:
        """Move cursor down."""
        board = self.query_one(GameBoard)
        board.cursor_y = min(board.board_size - 1, board.cursor_y + 1)
        board.update_board()

    def action_move_left(self) -> None:
        """Move cursor left."""
        board = self.query_one(GameBoard)
        board.cursor_x = max(0, board.cursor_x - 1)
        board.update_board()

    def action_move_right(self) -> None:
        """Move cursor right."""
        board = self.query_one(GameBoard)
        board.cursor_x = min(board.board_size - 1, board.cursor_x + 1)
        board.update_board()

    def action_toggle_wall_above(self) -> None:
        """Toggle wall above cursor."""
        board = self.query_one(GameBoard)
        if board.cursor_y > 0:
            x, y = board.cursor_x, board.cursor_y - 1
            if board.board.has_horizontal_wall(x, y):
                board.board.remove_horizontal_wall(x, y)
            else:
                board.board.add_horizontal_wall(x, y)
            board.update_board()

    def action_toggle_wall_below(self) -> None:
        """Toggle wall below cursor."""
        board = self.query_one(GameBoard)
        if board.cursor_y < board.board_size - 1:
            x, y = board.cursor_x, board.cursor_y
            if board.board.has_horizontal_wall(x, y):
                board.board.remove_horizontal_wall(x, y)
            else:
                board.board.add_horizontal_wall(x, y)
            board.update_board()

    def action_toggle_wall_left(self) -> None:
        """Toggle wall to left of cursor."""
        board = self.query_one(GameBoard)
        if board.cursor_x > 0:
            x, y = board.cursor_x - 1, board.cursor_y
            if board.board.has_vertical_wall(x, y):
                board.board.remove_vertical_wall(x, y)
            else:
                board.board.add_vertical_wall(x, y)
            board.update_board()

    def action_toggle_wall_right(self) -> None:
        """Toggle wall to right of cursor."""
        board = self.query_one(GameBoard)
        if board.cursor_x < board.board_size - 1:
            x, y = board.cursor_x, board.cursor_y
            if board.board.has_vertical_wall(x, y):
                board.board.remove_vertical_wall(x, y)
            else:
                board.board.add_vertical_wall(x, y)
            board.update_board()
