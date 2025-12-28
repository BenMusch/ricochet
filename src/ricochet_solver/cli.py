"""CLI entry point for ricochet-solver."""

import sys

from ricochet_solver.app import RicochetSolverApp


def main() -> int:
    """Main CLI entry point."""
    app = RicochetSolverApp()
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
