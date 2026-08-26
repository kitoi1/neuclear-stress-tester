"""Unit tests for the test runner."""

from neuclear.config import Config
from neuclear.runner import (
    TestRunner,
    create_runner_from_config,
)


def test_runner_creation():
    """Test TestRunner creation."""

    config = Config(
        target_url="http://localhost:8080",
        workers=1,
        rate=1,
        duration="1s",
    )

    runner = TestRunner(config)

    assert runner.config is config
    assert runner.results == []


def test_create_runner_from_config():
    """Test runner factory."""

    config = Config(
        target_url="http://localhost:8080"
    )

    runner = create_runner_from_config(
        config
    )

    assert isinstance(
        runner,
        TestRunner,
    )

    assert runner.config is config