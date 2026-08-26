"""Unit tests for configuration."""

import pytest

from neuclear.config import Config


def test_config_creation():
    """Test basic config creation."""

    config = Config(
        target_url="http://example.com",
        workers=4,
        rate=1000,
        duration="30s",
    )

    assert config.target_url == "http://example.com"
    assert config.workers == 4
    assert config.rate == 1000
    assert config.total_rate == 4000
    assert config.duration_seconds == 30


def test_invalid_url():
    """Test invalid URL handling."""

    with pytest.raises(ValueError):
        Config(target_url="example.com")


def test_duration_conversion():
    """Test duration string to seconds conversion."""

    config = Config(
        target_url="http://example.com",
        duration="1m",
    )

    assert config.duration_seconds == 60

    config = Config(
        target_url="http://example.com",
        duration="2h",
    )

    assert config.duration_seconds == 7200


def test_invalid_workers():
    """Test that workers must be positive."""

    with pytest.raises(ValueError):
        Config(
            target_url="http://example.com",
            workers=0,
        )


def test_invalid_rate():
    """Test that rate must be positive."""

    with pytest.raises(ValueError):
        Config(
            target_url="http://example.com",
            rate=0,
        )


def test_invalid_timeout():
    """Test that timeout must be positive."""

    with pytest.raises(ValueError):
        Config(
            target_url="http://example.com",
            timeout=0,
        )


def test_http_methods_are_normalized():
    """Test that HTTP methods are converted to uppercase."""

    config = Config(
        target_url="http://example.com",
        method="post",
    )

    assert config.method == "POST"


def test_invalid_http_method():
    """Test that unsupported HTTP methods are rejected."""

    with pytest.raises(ValueError):
        Config(
            target_url="http://example.com",
            method="INVALID",
        )


def test_duration_property():
    """Test different duration units."""

    assert Config(
        target_url="http://example.com",
        duration="10s",
    ).duration_seconds == 10

    assert Config(
        target_url="http://example.com",
        duration="5m",
    ).duration_seconds == 300

    assert Config(
        target_url="http://example.com",
        duration="2h",
    ).duration_seconds == 7200


def test_invalid_duration():
    """Test invalid duration formats."""

    with pytest.raises(ValueError):
        Config(
            target_url="http://example.com",
            duration="invalid",
        )


def test_total_rate():
    """Test total configured request rate."""

    config = Config(
        target_url="http://example.com",
        workers=5,
        rate=200,
    )

    assert config.total_rate == 1000


def test_to_dict():
    """Test conversion to dictionary."""

    config = Config(
        target_url="http://example.com",
        workers=2,
        rate=50,
        duration="10s",
    )

    data = config.to_dict()

    assert data["target_url"] == "http://example.com"
    assert data["workers"] == 2
    assert data["rate"] == 50
    assert data["duration"] == "10s"
    assert data["total_rate"] == 100
    assert data["duration_seconds"] == 10