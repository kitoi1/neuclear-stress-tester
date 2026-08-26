"""Unit tests for the command-line interface."""

from typer.testing import CliRunner

from neuclear.cli import app


runner = CliRunner()


def test_help():
    """Test CLI help output."""

    result = runner.invoke(
        app,
        ["--help"],
    )

    assert result.exit_code == 0
    assert "test" in result.stdout
    assert "analyze" in result.stdout
    assert "version" in result.stdout


def test_version():
    """Test version command."""

    result = runner.invoke(
        app,
        ["version"],
    )

    assert result.exit_code == 0
    assert "4.1.0" in result.stdout


def test_list_presets():
    """Test benchmark presets command."""

    result = runner.invoke(
        app,
        ["list-presets"],
    )

    assert result.exit_code == 0
    assert "light" in result.stdout
    assert "medium" in result.stdout
    assert "heavy" in result.stdout


def test_invalid_url():
    """Test invalid URL handling."""

    result = runner.invoke(
        app,
        [
            "test",
            "ftp://example.com",
        ],
    )

    assert result.exit_code != 0
    assert "Invalid URL" in result.stdout