from neuclear.utils import (
    format_duration,
    parse_duration,
    validate_url,
)


def test_valid_urls():
    assert validate_url(
        "http://localhost:8080"
    )

    assert validate_url(
        "https://example.com"
    )

    assert validate_url(
        "http://127.0.0.1:8080/test"
    )


def test_invalid_urls():
    assert not validate_url(
        "localhost:8080"
    )

    assert not validate_url(
        "ftp://example.com"
    )

    assert not validate_url(
        "not-a-url"
    )


def test_parse_duration():
    assert parse_duration("10s") == 10
    assert parse_duration("2m") == 120
    assert parse_duration("1h") == 3600


def test_format_duration():
    assert format_duration(10) == "10.0s"
    assert format_duration(120) == "2.0m"
