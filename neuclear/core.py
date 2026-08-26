"""
Core asynchronous HTTP load-testing engine.
"""

import asyncio
import time

import aiohttp
from rich.console import Console

from .config import Config
from .models import RequestResult, TestResult


console = Console()


class StressTest:
    """Asynchronous HTTP load-test orchestrator."""

    def __init__(
        self,
        config: Config,
    ) -> None:
        self.config = config
        self.results = TestResult()

        self._stop_event = asyncio.Event()
        self._worker_end_time = 0.0

    def stop(self) -> None:
        """Request a graceful stop."""

        self._stop_event.set()

    async def make_request(
        self,
        session: aiohttp.ClientSession,
    ) -> RequestResult:
        """Perform a single HTTP request."""

        start = time.monotonic()

        try:
            async with session.request(
                method=self.config.method,
                url=self.config.target_url,
                headers=(
                    self.config.headers
                    or None
                ),
                data=self.config.payload,
            ) as response:

                # Consume the response body so that aiohttp
                # can safely reuse the connection.
                await response.read()

                latency_ms = (
                    time.monotonic()
                    - start
                ) * 1000.0

                return RequestResult(
                    success=response.status < 400,
                    status_code=response.status,
                    latency_ms=latency_ms,
                )

        except asyncio.CancelledError:
            raise

        except Exception as exc:
            latency_ms = (
                time.monotonic()
                - start
            ) * 1000.0

            return RequestResult(
                success=False,
                status_code=0,
                latency_ms=latency_ms,
                error=(
                    f"{type(exc).__name__}: "
                    f"{exc}"
                ),
            )

    async def worker(
        self,
        worker_id: int,
    ) -> TestResult:
        """Run one asynchronous load worker."""

        # Currently unused, but retained so worker-specific
        # metrics can be added later.
        del worker_id

        local_results = TestResult()

        timeout = aiohttp.ClientTimeout(
            total=self.config.timeout
        )

        connector = aiohttp.TCPConnector(
            limit=self.config.connection_limit,
            enable_cleanup_closed=True,
        )

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
        ) as session:

            interval = (
                1.0 / self.config.rate
            )

            next_request_time = (
                time.monotonic()
            )

            while not self._stop_event.is_set():

                if (
                    time.monotonic()
                    >= self._worker_end_time
                ):
                    break

                result = await self.make_request(
                    session
                )

                local_results.total_requests += 1

                local_results.latencies.append(
                    result.latency_ms
                )

                if result.success:
                    local_results.successful += 1

                    local_results.status_codes[
                        result.status_code
                    ] = (
                        local_results.status_codes.get(
                            result.status_code,
                            0,
                        )
                        + 1
                    )

                else:
                    local_results.failed += 1

                    error_key = (
                        result.error
                        if result.error
                        else (
                            f"HTTP "
                            f"{result.status_code}"
                        )
                    )

                    local_results.errors[
                        error_key
                    ] = (
                        local_results.errors.get(
                            error_key,
                            0,
                        )
                        + 1
                    )

                    if result.status_code:
                        local_results.status_codes[
                            result.status_code
                        ] = (
                            local_results.status_codes.get(
                                result.status_code,
                                0,
                            )
                            + 1
                        )

                # Schedule the next request from a
                # monotonic clock to maintain the
                # configured rate.
                next_request_time += interval

                sleep_for = (
                    next_request_time
                    - time.monotonic()
                )

                if sleep_for > 0:
                    await asyncio.sleep(
                        sleep_for
                    )

                elif (
                    time.monotonic()
                    - next_request_time
                    > interval * 10
                ):
                    # If the worker falls significantly
                    # behind schedule, reset instead of
                    # generating a burst of requests.
                    next_request_time = (
                        time.monotonic()
                    )

        return local_results

    async def run(self) -> TestResult:
        """Run the complete stress test."""

        console.print(
            "[cyan]"
            "Starting stress test with "
            f"{self.config.workers} workers..."
            "[/cyan]"
        )

        self.results = TestResult()

        self._stop_event.clear()

        self.results.start_time = (
            time.monotonic()
        )

        self._worker_end_time = (
            self.results.start_time
            + self.config.duration_seconds
        )

        tasks = [
            asyncio.create_task(
                self.worker(worker_id)
            )
            for worker_id in range(
                self.config.workers
            )
        ]

        worker_results = []

        try:
            worker_results = await asyncio.gather(
                *tasks
            )

        except asyncio.CancelledError:
            self.stop()

            for task in tasks:
                if not task.done():
                    task.cancel()

            await asyncio.gather(
                *tasks,
                return_exceptions=True,
            )

            raise

        finally:
            self.results.end_time = (
                time.monotonic()
            )

        for result in worker_results:
            self.results.merge(result)

        return self.results