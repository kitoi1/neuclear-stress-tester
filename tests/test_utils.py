"""Unit tests for utility functions."""

import pytest

from neuclear.utils import (
    format_duration,
    parse_duration,
    validate_url,
)


def test_validate_url():
    """Test HTTP and HTTPS URL validation."""

    assert (
        validate_url(
            "http://example.com"
        )
        is True
    )

    assert (
        validate_url(
            "https://example.com"
        )
        is True
    )

    assert (
        validate_url(
            "ftp://example.com"
        )
        is False
    )

    assert (
        validate_url(
            "example.com"
        )
        is False
    )

    assert (
        validate_url(
            ""
        )
        is False
    )


def test_format_duration():
    """Test human-readable duration formatting."""

    assert (
        format_duration(10)
        == "10.0s"
    )

    assert (
        format_duration(60)
        == "1.0m"
    )

    assert (
        format_duration(3600)
        == "1.0h"
    )


def test_parse_duration():
    """Test duration parsing."""

    assert (
        parse_duration("10s")
        == 10
    )

    assert (
        parse_duration("2m")
        == 120
    )

    assert (
        parse_duration("1h")
        == 3600
    )


def test_invalid_duration():
    """Test invalid duration strings."""

    with pytest.raises(ValueError):
        parse_duration("10")

    with pytest.raises(ValueError):
        parse_duration("10d")

    with pytest.raises(ValueError):
        parse_duration("abc")