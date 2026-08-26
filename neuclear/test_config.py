import pytest

from neuclear.config import Config


def test_duration_seconds():
    assert Config(
        target_url="http://localhost:8080",
        duration="10s",
    ).duration_seconds == 10

    assert Config(
        target_url="http://localhost:8080",
        duration="2m",
    ).duration_seconds == 120

    assert Config(
        target_url="http://localhost:8080",
        duration="1h",
    ).duration_seconds == 3600


def test_total_rate():
    config = Config(
        target_url="http://localhost:8080",
        workers=4,
        rate=100,
    )

    assert config.total_rate == 400


def test_invalid_url():
    with pytest.raises(ValueError):
        Config(
            target_url="localhost:8080"
        )


def test_invalid_workers():
    with pytest.raises(ValueError):
        Config(
            target_url="http://localhost:8080",
            workers=0,
        )


def test_invalid_rate():
    with pytest.raises(ValueError):
        Config(
            target_url="http://localhost:8080",
            rate=0,
        )


def test_invalid_duration():
    with pytest.raises(ValueError):
        Config(
            target_url="http://localhost:8080",
            duration="invalid",
        )


def test_invalid_method():
    with pytest.raises(ValueError):
        Config(
            target_url="http://localhost:8080",
            method="INVALID",
        )
