"""
Utility functions for Nuclear Stress Tester.
"""

import asyncio
import re
import socket
from typing import Tuple
from urllib.parse import urlparse

import psutil
from rich.console import Console


console = Console()


def validate_url(url: str) -> bool:
    """Validate an HTTP/HTTPS URL."""

    try:
        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            return False

        if not parsed.netloc:
            return False

        return True

    except Exception:
        return False


def format_duration(seconds: float) -> str:
    """Format seconds into a human-readable duration."""

    if seconds < 60:
        return f"{seconds:.1f}s"

    if seconds < 3600:
        return f"{seconds / 60:.1f}m"

    return f"{seconds / 3600:.1f}h"


def parse_duration(duration_str: str) -> float:
    """Parse duration strings such as 10s, 2m, or 1h."""

    match = re.match(
        r"^(\d+(?:\.\d+)?)([smh])$",
        duration_str,
    )

    if not match:
        raise ValueError(
            "Duration must be like 10s, 2m, or 1h"
        )

    value, unit = match.groups()

    multipliers = {
        "s": 1,
        "m": 60,
        "h": 3600,
    }

    return float(value) * multipliers[unit]


def get_system_info() -> dict:
    """Return basic system information."""

    memory = psutil.virtual_memory()

    return {
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_total": memory.total,
        "memory_available": memory.available,
    }


def is_port_open(
    host: str,
    port: int,
    timeout: float = 2.0,
) -> bool:
    """Check whether a TCP port is accepting connections."""

    try:
        with socket.create_connection(
            (host, port),
            timeout=timeout,
        ):
            return True

    except (
        socket.timeout,
        ConnectionRefusedError,
        OSError,
    ):
        return False


async def async_is_port_open(
    host: str,
    port: int,
    timeout: float = 2.0,
) -> bool:
    """Asynchronously check whether a TCP port is open."""

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout,
        )

        writer.close()
        await writer.wait_closed()

        return True

    except (
        asyncio.TimeoutError,
        ConnectionRefusedError,
        OSError,
    ):
        return False


def check_system_limits(
    workers: int,
    rate: int,
) -> Tuple[bool, str]:
    """Check whether requested load is reasonable locally."""

    cpu_count = psutil.cpu_count() or 1
    memory = psutil.virtual_memory()

    warnings = []

    if workers > cpu_count * 4:
        warnings.append(
            f"workers ({workers}) exceed "
            f"CPU count × 4 ({cpu_count * 4})"
        )

    estimated_memory = (
        workers * 10 * 1024 * 1024
    )

    if estimated_memory > memory.available * 0.5:
        warnings.append(
            "estimated worker memory usage is high"
        )

    total_rate = workers * rate

    if total_rate > 100_000:
        warnings.append(
            f"total rate ({total_rate:,} RPS) "
            "is extremely high"
        )

    if warnings:
        return False, " | ".join(warnings)

    return True, "OK"


def print_banner() -> None:
    """Print the Nuclear banner."""

    banner = r"""
 _   _ _   _ _ _ _   _           _____ _                 _____
| \ | | |_(_) (_) |_(_)_ __ ___ |_   _| |__   ___ _ __  |_   _|
|  \| | __| | | | __| | '_ ` _ \  | | | '_ \ / _ \ '__|   | |
| |\  | |_| | | | |_| | | | | | | | | | | | |  __/ |      | |
|_| \_|\__|_|_|_|\__|_|_| |_| |_| |_| |_| |_|\___|_|      |_|

          💣 Nuclear Stress Tester v4.1
"""

    console.print(
        f"[magenta]{banner}[/magenta]"
    )
