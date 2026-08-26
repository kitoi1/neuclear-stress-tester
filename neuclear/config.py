"""
Configuration management for Nuclear Stress Tester.
"""

import json
import re
from dataclasses import asdict, dataclass, field
from typing import Dict, Optional


DURATION_PATTERN = re.compile(r"^(\d+(?:\.\d+)?)([smh])$")


@dataclass
class Config:
    """Configuration for a stress test."""

    target_url: str

    workers: int = 1
    rate: int = 10
    duration: str = "10s"

    output_file: str = "report.json"

    timeout: float = 30.0

    method: str = "GET"

    headers: Dict[str, str] = field(default_factory=dict)

    payload: Optional[str] = None

    connection_limit: int = 100

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Validate configuration values."""

        if not re.match(r"^https?://", self.target_url):
            raise ValueError(
                "URL must start with http:// or https://"
            )

        if self.workers <= 0:
            raise ValueError("Workers must be positive")

        if self.rate <= 0:
            raise ValueError("Rate must be positive")

        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")

        if self.connection_limit <= 0:
            raise ValueError(
                "Connection limit must be positive"
            )

        if not DURATION_PATTERN.match(self.duration):
            raise ValueError(
                "Duration must be like '10s', '1m', or '2h'"
            )

        self.method = self.method.upper()

        allowed_methods = {
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "HEAD",
            "OPTIONS",
        }

        if self.method not in allowed_methods:
            raise ValueError(
                f"Unsupported HTTP method: {self.method}"
            )

    @property
    def duration_seconds(self) -> float:
        """Convert duration into seconds."""

        match = DURATION_PATTERN.match(self.duration)

        if not match:
            raise ValueError(
                f"Invalid duration: {self.duration}"
            )

        value, unit = match.groups()

        value = float(value)

        multipliers = {
            "s": 1,
            "m": 60,
            "h": 3600,
        }

        return value * multipliers[unit]

    @property
    def total_rate(self) -> int:
        """Total configured requests per second."""

        return self.workers * self.rate

    def to_dict(self) -> dict:
        data = asdict(self)
        data["total_rate"] = self.total_rate
        data["duration_seconds"] = self.duration_seconds
        return data

    def save(self, filename: str) -> None:
        """Save configuration to JSON."""

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=2)

    @classmethod
    def load(cls, filename: str) -> "Config":
        """Load configuration from JSON."""

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        allowed_fields = {
            "target_url",
            "workers",
            "rate",
            "duration",
            "output_file",
            "timeout",
            "method",
            "headers",
            "payload",
            "connection_limit",
        }

        filtered = {
            key: value
            for key, value in data.items()
            if key in allowed_fields
        }

        return cls(**filtered)


def create_default_config() -> Config:
    """Create a safe local-development configuration."""

    return Config(
        target_url="http://localhost:8080",
        workers=1,
        rate=10,
        duration="10s",
        output_file="stress_test_report.json",
        timeout=30,
    )
