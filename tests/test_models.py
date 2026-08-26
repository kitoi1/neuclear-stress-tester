"""Unit tests for result models."""

from neuclear.models import (
    RequestResult,
    TestResult,
)


def test_request_result():
    """Test RequestResult creation."""

    result = RequestResult(
        success=True,
        status_code=200,
        latency_ms=25.5,
    )

    assert result.success is True
    assert result.status_code == 200
    assert result.latency_ms == 25.5
    assert result.error == ""


def test_test_result_rates():
    """Test success and failure rates."""

    result = TestResult(
        total_requests=10,
        successful=8,
        failed=2,
    )

    assert result.success_rate == 80.0
    assert result.failure_rate == 20.0


def test_test_result_percentiles():
    """Test latency percentile calculations."""

    result = TestResult(
        latencies=[
            10.0,
            20.0,
            30.0,
            40.0,
            50.0,
        ]
    )

    assert result.min_latency == 10.0
    assert result.max_latency == 50.0
    assert result.p50_latency == 30.0
    assert result.p95_latency > 40.0
    assert result.p99_latency > 40.0


def test_test_result_merge():
    """Test merging two result objects."""

    first = TestResult(
        total_requests=10,
        successful=8,
        failed=2,
        latencies=[
            10.0,
            20.0,
        ],
        status_codes={
            200: 8,
            500: 2,
        },
    )

    second = TestResult(
        total_requests=5,
        successful=4,
        failed=1,
        latencies=[
            30.0,
        ],
        status_codes={
            200: 4,
            500: 1,
        },
    )

    first.merge(second)

    assert first.total_requests == 15
    assert first.successful == 12
    assert first.failed == 3
    assert first.latencies == [
        10.0,
        20.0,
        30.0,
    ]

    assert first.status_codes[200] == 12
    assert first.status_codes[500] == 3


def test_empty_result():
    """Test empty result behavior."""

    result = TestResult()

    assert result.success_rate == 0.0
    assert result.failure_rate == 0.0
    assert result.avg_latency == 0.0
    assert result.min_latency == 0.0
    assert result.max_latency == 0.0
    assert result.p95_latency == 0.0
    assert result.p99_latency == 0.0
    assert result.requests_per_second == 0.0