from typer.testing import CliRunner

from neuclear.cli import app


runner = CliRunner()


def test_help():
    result = runner.invoke(
        app,
        ["--help"],
    )

    assert result.exit_code == 0
    assert "Nuclear Stress Tester" in result.stdout


def test_list_presets():
    result = runner.invoke(
        app,
        ["list-presets"],
    )

    assert result.exit_code == 0
    assert "light" in result.stdout
    assert "medium" in result.stdout
    assert "heavy" in result.stdout


def test_version():
    result = runner.invoke(
        app,
        ["version"],
    )

    assert result.exit_code == 0
    assert "4.1.0" in result.stdout


def test_invalid_url():
    result = runner.invoke(
        app,
        [
            "test",
            "not-a-url",
        ],
    )

    assert result.exit_code != 0
