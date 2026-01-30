"""Unit tests for configuration"""

import pytest
from neuclear.config import Config

def test_config_creation():
    """Test basic config creation"""
    config = Config(
        target_url="http://example.com",
        processes=4,
        rate=1000,
        duration="30s",
    )
    
    assert config.target_url == "http://example.com"
    assert config.processes == 4
    assert config.rate == 1000
    assert config.total_rate == 4000
    assert config.duration_seconds == 30

def test_invalid_url():
    """Test invalid URL handling"""
    with pytest.raises(ValueError):
        Config(target_url="example.com")

def test_duration_conversion():
    """Test duration string to seconds conversion"""
    config = Config(target_url="http://example.com", duration="1m")
    assert config.duration_seconds == 60
    
    config = Config(target_url="http://example.com", duration="2h")
    assert config.duration_seconds == 7200