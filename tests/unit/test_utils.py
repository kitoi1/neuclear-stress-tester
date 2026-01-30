"""Unit tests for utility functions"""

import pytest
from neuclear.utils import validate_url, format_duration, parse_duration

def test_validate_url():
    """Test URL validation"""
    assert validate_url("http://example.com") is True
    assert validate_url("https://example.com") is True
    assert validate_url("ftp://example.com") is True
    assert validate_url("example.com") is False
    assert validate_url("://example.com") is False

def test_format_duration():
    """Test duration formatting"""
    assert format_duration(30) == "30.0s"
    assert format_duration(90) == "1.5m"
    assert format_duration(7200) == "2.0h"

def test_parse_duration():
    """Test duration parsing"""
    assert parse_duration("30s") == 30
    assert parse_duration("1m") == 60
    assert parse_duration("2h") == 7200
    
    with pytest.raises(ValueError):
        parse_duration("30")