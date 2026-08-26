"""
Data models used by Nuclear Stress Tester.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class RequestResult:
    """Result of a single HTTP request."""

    success: bool
    status_code: int
    latency_ms: float
    error: str = ""


@dataclass
class TestResult:
    """Aggregated results from a stress test."""

    total_requests: int = 0
    successful: int = 0
    failed: int = 0

    status_codes: Dict[int, int] = field(
        default_factory=dict
    )

    # Store latency for every request, including failures.
    latencies: List[float] = field(
        default_factory=list
    )

    errors: Dict[str, int] = field(
        default_factory=dict
    )

    start_time: float = 0.0
    end_time: float = 0.0

    @property
    def duration_seconds(self) -> float:
        """Return test duration in seconds."""

        return max(
            0.0,
            self.end_time - self.start_time,
        )

    @property
    def success_rate(self) -> float:
        """Return percentage of successful requests."""

        if self.total_requests == 0:
            return 0.0

        return (
            self.successful
            / self.total_requests
        ) * 100.0

    @property
    def failure_rate(self) -> float:
        """Return percentage of failed requests."""

        if self.total_requests == 0:
            return 0.0

        return (
            self.failed
            / self.total_requests
        ) * 100.0

    @property
    def avg_latency(self) -> float:
        """Return average request latency in milliseconds."""

        if not self.latencies:
            return 0.0

        return sum(self.latencies) / len(
            self.latencies
        )

    @property
    def min_latency(self) -> float:
        """Return minimum request latency."""

        if not self.latencies:
            return 0.0

        return min(self.latencies)

    @property
    def max_latency(self) -> float:
        """Return maximum request latency."""

        if not self.latencies:
            return 0.0

        return max(self.latencies)

    def percentile(
        self,
        percentile: float,
    ) -> float:
        """
        Calculate a percentile using linear interpolation.

        This implementation does not require an external
        statistics package and works correctly with small
        sample sizes.
        """

        if not self.latencies:
            return 0.0

        if not 0 <= percentile <= 100:
            raise ValueError(
                "Percentile must be between 0 and 100"
            )

        values = sorted(self.latencies)

        if len(values) == 1:
            return values[0]

        position = (
            (len(values) - 1)
            * (percentile / 100.0)
        )

        lower = int(position)

        upper = min(
            lower + 1,
            len(values) - 1,
        )

        fraction = position - lower

        return (
            values[lower]
            + (
                values[upper]
                - values[lower]
            )
            * fraction
        )

    @property
    def p50_latency(self) -> float:
        """Return the 50th percentile latency."""

        return self.percentile(50)

    @property
    def p90_latency(self) -> float:
        """Return the 90th percentile latency."""

        return self.percentile(90)

    @property
    def p95_latency(self) -> float:
        """Return the 95th percentile latency."""

        return self.percentile(95)

    @property
    def p99_latency(self) -> float:
        """Return the 99th percentile latency."""

        return self.percentile(99)

    @property
    def requests_per_second(self) -> float:
        """Return actual requests per second."""

        if self.duration_seconds <= 0:
            return 0.0

        return (
            self.total_requests
            / self.duration_seconds
        )

    @property
    def rps(self) -> float:
        """Backwards-compatible alias for requests_per_second."""

        return self.requests_per_second

    def merge(
        self,
        other: "TestResult",
    ) -> None:
        """Merge another TestResult into this result."""

        self.total_requests += (
            other.total_requests
        )

        self.successful += (
            other.successful
        )

        self.failed += other.failed

        self.latencies.extend(
            other.latencies
        )

        for status_code, count in (
            other.status_codes.items()
        ):
            self.status_codes[
                status_code
            ] = (
                self.status_codes.get(
                    status_code,
                    0,
                )
                + count
            )

        for error, count in (
            other.errors.items()
        ):
            self.errors[error] = (
                self.errors.get(
                    error,
                    0,
                )
                + count
            )

    def to_dict(self) -> dict:
        """Convert results to a JSON-compatible dictionary."""

        return {
            "total_requests": self.total_requests,
            "successful": self.successful,
            "failed": self.failed,
            "success_rate": round(
                self.success_rate,
                4,
            ),
            "failure_rate": round(
                self.failure_rate,
                4,
            ),
            "requests_per_second": round(
                self.requests_per_second,
                4,
            ),
            "duration_seconds": round(
                self.duration_seconds,
                4,
            ),
            "latency_ms": {
                "min": round(
                    self.min_latency,
                    4,
                ),
                "avg": round(
                    self.avg_latency,
                    4,
                ),
                "p50": round(
                    self.p50_latency,
                    4,
                ),
                "p90": round(
                    self.p90_latency,
                    4,
                ),
                "p95": round(
                    self.p95_latency,
                    4,
                ),
                "p99": round(
                    self.p99_latency,
                    4,
                ),
                "max": round(
                    self.max_latency,
                    4,
                ),
            },
            "status_codes": {
                str(code): count
                for code, count
                in self.status_codes.items()
            },
            "errors": self.errors,
        }

    def save_report(
        self,
        filename: str,
    ) -> None:
        """Save the result as a JSON report."""

        import json

        with open(
            filename,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.to_dict(),
                file,
                indent=2,
            )