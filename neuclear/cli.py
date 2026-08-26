"""
Command-line interface for Nuclear Stress Tester.
"""

import asyncio
import json
from typing import List, Optional

import psutil
import typer
from rich.console import Console
from rich.table import Table

from .config import Config
from .core import StressTest
from .utils import (
    check_system_limits,
    validate_url,
)


app = typer.Typer(
    name="neuclear",
    help=(
        "Nuclear Stress Tester - "
        "controlled HTTP load testing"
    ),
    add_completion=False,
)

console = Console()


@app.command()
def test(
    url: str = typer.Argument(
        ...,
        help="Target HTTP/HTTPS URL.",
    ),
    workers: int = typer.Option(
        1,
        "--workers",
        "-w",
        min=1,
        max=100,
        help="Number of asynchronous workers.",
    ),
    rate: int = typer.Option(
        10,
        "--rate",
        "-r",
        min=1,
        max=10000,
        help=(
            "Requests per second per worker."
        ),
    ),
    duration: str = typer.Option(
        "10s",
        "--duration",
        "-d",
        help=(
            "Duration, e.g. 10s, 1m, 2h."
        ),
    ),
    output: str = typer.Option(
        "report.json",
        "--output",
        "-o",
        help="JSON report output.",
    ),
    timeout: float = typer.Option(
        30.0,
        "--timeout",
        "-t",
        min=0.1,
        help="HTTP request timeout in seconds.",
    ),
    method: str = typer.Option(
        "GET",
        "--method",
        "-m",
        help="HTTP method.",
    ),
    header: Optional[List[str]] = typer.Option(
        None,
        "--header",
        "-H",
        help=(
            "HTTP header in "
            "'Name: Value' format."
        ),
    ),
    body: Optional[str] = typer.Option(
        None,
        "--body",
        help="HTTP request body.",
    ),
    connection_limit: int = typer.Option(
        100,
        "--connection-limit",
        min=1,
        help=(
            "Maximum simultaneous "
            "connections per worker."
        ),
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress progress messages.",
    ),
):
    """Run a controlled HTTP stress test."""

    if not validate_url(url):
        console.print(
            "[red]Invalid URL.[/red] "
            "Use http:// or https://."
        )

        raise typer.Exit(1)

    method = method.upper()

    headers = {}

    if header:
        for item in header:

            if ":" not in item:
                console.print(
                    "[red]Invalid header:[/red] "
                    f"{item}. "
                    "Use 'Name: Value'."
                )

                raise typer.Exit(1)

            name, value = item.split(
                ":",
                1,
            )

            name = name.strip()
            value = value.strip()

            if not name:
                console.print(
                    "[red]Header name "
                    "cannot be empty.[/red]"
                )

                raise typer.Exit(1)

            headers[name] = value

    total_rate = (
        workers * rate
    )

    if total_rate > 100_000:
        console.print(
            "[red]"
            "Requested total rate is "
            "extremely high."
            "[/red]"
        )

        console.print(
            f"Requested: {total_rate:,} RPS"
        )

        console.print(
            "Reduce --workers or --rate."
        )

        raise typer.Exit(1)

    cpu_count = (
        psutil.cpu_count() or 1
    )

    if workers > cpu_count * 4:
        console.print(
            "[yellow]Warning:[/yellow] "
            f"{workers} workers on "
            f"{cpu_count} CPU cores."
        )

    safe, warning = check_system_limits(
        workers,
        rate,
    )

    if not safe and warning != "OK":
        console.print(
            "[yellow]System warning:[/yellow] "
            f"{warning}"
        )

    try:
        config = Config(
            target_url=url,
            workers=workers,
            rate=rate,
            duration=duration,
            output_file=output,
            timeout=timeout,
            method=method,
            headers=headers,
            payload=body,
            connection_limit=(
                connection_limit
            ),
        )

    except ValueError as exc:
        console.print(
            "[red]Configuration error:[/red] "
            f"{exc}"
        )

        raise typer.Exit(1)

    if not quiet:
        console.print(
            "[bold magenta]"
            "Nuclear Stress Tester v4.1"
            "[/bold magenta]"
        )

        console.print(
            f"[cyan]Target:[/cyan] {url}"
        )

        console.print(
            f"[cyan]Workers:[/cyan] "
            f"{workers}"
        )

        console.print(
            "[cyan]Rate:[/cyan] "
            f"{rate} RPS/worker "
            f"(total {total_rate} RPS)"
        )

        console.print(
            "[cyan]Duration:[/cyan] "
            f"{duration}"
        )

        console.print(
            "[cyan]Method:[/cyan] "
            f"{method}"
        )

        console.print(
            "[cyan]Timeout:[/cyan] "
            f"{timeout}s"
        )

    tester = StressTest(
        config
    )

    try:
        results = asyncio.run(
            tester.run()
        )

    except KeyboardInterrupt:
        tester.stop()

        console.print(
            "\n[yellow]"
            "Test interrupted."
            "[/yellow]"
        )

        raise typer.Exit(130)

    try:
        results.save_report(
            output
        )

    except OSError as exc:
        console.print(
            "[red]Could not write "
            "report:[/red] "
            f"{exc}"
        )

        raise typer.Exit(1)

    console.print("")

    table = Table(
        title="Test Results",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Metric")
    table.add_column("Value")

    table.add_row(
        "Requests",
        f"{results.total_requests:,}",
    )

    table.add_row(
        "Successful",
        f"{results.successful:,}",
    )

    table.add_row(
        "Failed",
        f"{results.failed:,}",
    )

    table.add_row(
        "Success rate",
        f"{results.success_rate:.2f}%",
    )

    table.add_row(
        "Failure rate",
        f"{results.failure_rate:.2f}%",
    )

    table.add_row(
        "RPS",
        (
            f"{results.requests_per_second:.2f}"
        ),
    )

    table.add_row(
        "Min latency",
        f"{results.min_latency:.2f} ms",
    )

    table.add_row(
        "Avg latency",
        f"{results.avg_latency:.2f} ms",
    )

    table.add_row(
        "P50 latency",
        f"{results.p50_latency:.2f} ms",
    )

    table.add_row(
        "P95 latency",
        f"{results.p95_latency:.2f} ms",
    )

    table.add_row(
        "P99 latency",
        f"{results.p99_latency:.2f} ms",
    )

    table.add_row(
        "Max latency",
        f"{results.max_latency:.2f} ms",
    )

    console.print(table)

    console.print(
        f"\n[green]Report saved:[/green] "
        f"{output}"
    )


@app.command()
def analyze(
    report_file: str = typer.Argument(
        ...,
        help="JSON report file.",
    ),
):
    """Analyze an existing JSON report."""

    try:
        with open(
            report_file,
            "r",
            encoding="utf-8",
        ) as file:
            report = json.load(file)

    except FileNotFoundError:
        console.print(
            "[red]Report not found:[/red] "
            f"{report_file}"
        )

        raise typer.Exit(1)

    except json.JSONDecodeError as exc:
        console.print(
            "[red]Invalid JSON report:[/red] "
            f"{exc}"
        )

        raise typer.Exit(1)

    table = Table(
        title="Nuclear Test Analysis"
    )

    table.add_column("Metric")
    table.add_column("Value")

    table.add_row(
        "Total requests",
        str(
            report.get(
                "total_requests",
                0,
            )
        ),
    )

    table.add_row(
        "Successful",
        str(
            report.get(
                "successful",
                0,
            )
        ),
    )

    table.add_row(
        "Failed",
        str(
            report.get(
                "failed",
                0,
            )
        ),
    )

    table.add_row(
        "Success rate",
        (
            f"{report.get('success_rate', 0):.2f}%"
        ),
    )

    table.add_row(
        "Failure rate",
        (
            f"{report.get('failure_rate', 0):.2f}%"
        ),
    )

    table.add_row(
        "RPS",
        (
            f"{report.get('requests_per_second', 0):.2f}"
        ),
    )

    latency = report.get(
        "latency_ms",
        {},
    )

    table.add_row(
        "Minimum latency",
        f"{latency.get('min', 0):.2f} ms",
    )

    table.add_row(
        "Average latency",
        f"{latency.get('avg', 0):.2f} ms",
    )

    table.add_row(
        "P50 latency",
        f"{latency.get('p50', 0):.2f} ms",
    )

    table.add_row(
        "P95 latency",
        f"{latency.get('p95', 0):.2f} ms",
    )

    table.add_row(
        "P99 latency",
        f"{latency.get('p99', 0):.2f} ms",
    )

    table.add_row(
        "Maximum latency",
        f"{latency.get('max', 0):.2f} ms",
    )

    console.print(table)


@app.command()
def list_presets():
    """List recommended benchmark presets."""

    table = Table(
        title="Benchmark Presets"
    )

    table.add_column("Preset")
    table.add_column("Workers")
    table.add_column("RPS/Worker")
    table.add_column("Duration")
    table.add_column("Purpose")

    presets = [
        (
            "light",
            1,
            10,
            "10s",
            "Local development",
        ),
        (
            "medium",
            2,
            50,
            "30s",
            "Staging",
        ),
        (
            "heavy",
            4,
            100,
            "60s",
            "Authorized performance test",
        ),
    ]

    for preset in presets:
        table.add_row(
            *map(str, preset)
        )

    console.print(table)


@app.command()
def version():
    """Show the current version."""

    console.print(
        "Nuclear Stress Tester v4.1.0"
    )


def main() -> None:
    """Application entry point."""

    app()


if __name__ == "__main__":
    main()