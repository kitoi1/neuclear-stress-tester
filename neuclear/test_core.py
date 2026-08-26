import asyncio

import pytest
from aiohttp import web

from neuclear.config import Config
from neuclear.core import StressTest


@pytest.fixture
async def test_server():
    async def handler(request):
        return web.json_response(
            {"status": "ok"}
        )

    app = web.Application()
    app.router.add_route(
        "*",
        "/",
        handler,
    )

    runner = web.AppRunner(app)

    await runner.setup()

    site = web.TCPSite(
        runner,
        "127.0.0.1",
        0,
    )

    await site.start()

    port = site._server.sockets[0].getsockname()[1]

    yield f"http://127.0.0.1:{port}/"

    await runner.cleanup()


@pytest.mark.asyncio
async def test_stress_test_runs(test_server):
    config = Config(
        target_url=test_server,
        workers=1,
        rate=5,
        duration="1s",
        timeout=5,
    )

    tester = StressTest(config)

    results = await tester.run()

    assert results.total_requests > 0
    assert results.successful > 0
    assert results.failed == 0
    assert results.requests_per_second > 0


@pytest.mark.asyncio
async def test_failed_connection():
    config = Config(
        target_url="http://127.0.0.1:1/",
        workers=1,
        rate=1,
        duration="1s",
        timeout=0.5,
    )

    tester = StressTest(config)

    results = await tester.run()

    assert results.total_requests > 0
    assert results.failed > 0
    assert len(results.latencies) > 0


def test_small_percentile_dataset():
    config = Config(
        target_url="http://localhost:8080"
    )

    tester = StressTest(config)

    tester.results.latencies = [10.0]

    assert tester.results.p95_latency == 10.0
    assert tester.results.p99_latency == 10.0
