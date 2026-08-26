"""
Test runner and worker orchestration.
"""

import asyncio
import time
from typing import List

from rich.live import Live
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table

from .config import Config
from .core import StressTest
from .models import TestResult
from .utils import (
    get_system_info,
    print_banner,
)


class TestRunner:
    """Orchestrates Nuclear Stress Tester runs."""

    def __init__(
        self,
        config: Config,
    ) -> None:
        self.config = config
        self.results: List[TestResult] = []

    async def run_single_test(
        self,
        test_config: Config,
    ) -> TestResult:
        """Run a single stress test."""

        stress_test = StressTest(
            test_config
        )

        return await stress_test.run()

    def run_concurrent_tests(
        self,
        configs: List[Config],
    ) -> List[TestResult]:
        """Run multiple configurations concurrently."""

        async def run_all() -> List[TestResult]:
            tasks = [
                self.run_single_test(config)
                for config in configs
            ]

            return await asyncio.gather(
                *tasks
            )

        return asyncio.run(
            run_all()
        )

    def run_with_progress(
        self,
    ) -> TestResult:
        """Run a test while displaying progress."""

        print_banner()

        with Progress(
            TextColumn(
                "[progress.description]"
                "{task.description}"
            ),
            BarColumn(),
            TextColumn(
                "[progress.percentage]"
                "{task.percentage:>3.0f}%"
            ),
            TimeRemainingColumn(),
        ) as progress:

            task = progress.add_task(
                (
                    "[cyan]Testing "
                    f"{self.config.target_url}..."
                ),
                total=(
                    self.config.duration_seconds
                ),
            )

            async def run_with_update() -> TestResult:
                stress_test = StressTest(
                    self.config
                )

                start_time = time.monotonic()

                test_task = asyncio.create_task(
                    stress_test.run()
                )

                while not test_task.done():

                    elapsed = (
                        time.monotonic()
                        - start_time
                    )

                    progress.update(
                        task,
                        completed=min(
                            elapsed,
                            self.config.duration_seconds,
                        ),
                    )

                    await asyncio.sleep(
                        0.1
                    )

                return await test_task

            result = asyncio.run(
                run_with_update()
            )

            progress.update(
                task,
                completed=(
                    self.config.duration_seconds
                ),
            )

        return result

    def monitor_system(
        self,
        interval: float = 1.0,
    ) -> None:
        """Monitor local system resources."""

        table = Table(
            title="System Monitoring"
        )

        table.add_column("Metric")
        table.add_column("Value")

        with Live(
            table,
            refresh_per_second=4,
        ) as live:

            try:
                while True:

                    info = get_system_info()

                    table.rows = []

                    table.add_row(
                        "CPU Count",
                        str(
                            info[
                                "cpu_count"
                            ]
                        ),
                    )

                    table.add_row(
                        "CPU Usage",
                        (
                            f"{info['cpu_percent']:.1f}%"
                        ),
                    )

                    table.add_row(
                        "Memory Available",
                        (
                            f"{info['memory_available'] / 1e9:.2f} GB"
                        ),
                    )

                    table.add_row(
                        "Network Connections",
                        str(
                            info[
                                "network_connections"
                            ]
                        ),
                    )

                    live.update(table)

                    time.sleep(interval)

            except KeyboardInterrupt:
                pass


def create_runner_from_config(
    config: Config,
) -> TestRunner:
    """Create a test runner from configuration."""

    return TestRunner(config)