"""Textual app for ricochet-solver."""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header, Static


class GameBoard(Static):
    """A game board widget."""

    def __init__(self) -> None:
        super().__init__()
        self.cursor_x = 0
        self.cursor_y = 0
        self.board_size = 16

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
            lines.append(" ".join(row))
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
