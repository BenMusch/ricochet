"""Tests for the CLI module."""

from ricochet_solver.cli import main


def test_main():
    """Test that main returns 0."""
    assert main() == 0
