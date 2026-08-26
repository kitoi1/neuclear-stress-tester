"""Unit tests for the core stress-testing engine."""

import asyncio

import pytest

from neuclear.config import Config
from neuclear.core import StressTest


@pytest.mark.asyncio
async def test_stress_test_can_stop():
    """Test that a stress test can be stopped."""

    config = Config(
        target_url="http://localhost:1",
        workers=1,
        rate=1,
        duration="1s",
        timeout=0.2,
    )

    tester = StressTest(config)

    tester.stop()

    assert tester._stop_event.is_set()


@pytest.mark.asyncio
async def test_stress_test_result_structure():
    """
    Test that the stress test returns the expected
    result structure.
    """

    config = Config(
        target_url="http://localhost:1",
        workers=1,
        rate=1,
        duration="0.1s",
        timeout=0.1,
    )

    tester = StressTest(config)

    result = await tester.run()

    assert result.total_requests >= 0
    assert result.successful >= 0
    assert result.failed >= 0
    assert (
        result.total_requests
        == result.successful
        + result.failed
    )