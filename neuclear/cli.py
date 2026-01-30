"""
CLI interface for Nuclear Stress Tester
"""

import typer
import asyncio
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer(
    name="neuclear",
    help="💣 Ultimate Nuclear Stress Tester - High-performance load testing tool",
    add_completion=False,
)
console = Console()

@app.command()
def test(
    url: str = typer.Argument(..., help="Target URL to stress test"),
    processes: int = typer.Option(4, "--processes", "-p", help="Number of processes"),
    rate: int = typer.Option(1000, "--rate", "-r", help="Requests per second per process"),
    duration: str = typer.Option("30s", "--duration", "-d", help="Test duration (e.g., 30s, 1m, 2h)"),
    output: str = typer.Option("report.json", "--output", "-o", help="Output report file"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress verbose output"),
):
    """
    Run a stress test against a target URL
    """
    # Import here to avoid circular imports
    from neuclear.utils import validate_url
    from neuclear.core import StressTest
    from neuclear.config import Config
    
    # Validate inputs
    if not validate_url(url):
        console.print("[red]Error: Invalid URL format. Include http:// or https://[/red]")
        raise typer.Exit(1)
    
    if processes <= 0:
        console.print("[red]Error: Number of processes must be positive[/red]")
        raise typer.Exit(1)
    
    if rate <= 0:
        console.print("[red]Error: Rate must be positive[/red]")
        raise typer.Exit(1)
    
    console.print(f"[bold magenta]💣 Nuclear Stress Tester v4.0[/bold magenta]")
    console.print(f"[cyan]Target:[/cyan] {url}")
    console.print(f"[cyan]Processes:[/cyan] {processes}")
    console.print(f"[cyan]Rate:[/cyan] {rate} RPS/process (Total: {processes * rate} RPS)")
    console.print(f"[cyan]Duration:[/cyan] {duration}")
    
    # Create config
    config = Config(
        target_url=url,
        processes=processes,
        rate=rate,
        duration=duration,
        output_file=output,
    )
    
    # Run stress test
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Starting stress test...", total=None)
        
        stress_test = StressTest(config)
        results = asyncio.run(stress_test.run())
        
        progress.update(task, completed=True, description="[green]Test complete!")
    
    # Display results
    console.print("\n[bold]Test Results:[/bold]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric")
    table.add_column("Value")
    
    table.add_row("Total Requests", str(results.total_requests))
    table.add_row("Successful", str(results.successful))
    table.add_row("Failed", str(results.failed))
    table.add_row("Success Rate", f"{results.success_rate:.2f}%")
    table.add_row("Average Latency", f"{results.avg_latency:.2f}ms")
    table.add_row("p95 Latency", f"{results.p95_latency:.2f}ms")
    table.add_row("p99 Latency", f"{results.p99_latency:.2f}ms")
    table.add_row("Requests/sec", f"{results.rps:.2f}")
    
    console.print(table)
    
    if output:
        results.save_report(output)
        console.print(f"[green]Report saved to: {output}[/green]")

@app.command()
def analyze(
    report_file: str = typer.Argument(..., help="Report file to analyze"),
):
    """
    Analyze an existing test report
    """
    console.print(f"[cyan]Analyzing report: {report_file}[/cyan]")
    console.print("[yellow]Report analysis feature coming soon![/yellow]")

@app.command()
def list_presets():
    """
    List available test presets
    """
    console.print("[bold magenta]Available Test Presets:[/bold magenta]")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Preset")
    table.add_column("Processes")
    table.add_column("Rate")
    table.add_column("Duration")
    table.add_column("Description")
    
    presets = [
        ("light", 2, 500, "30s", "Light load for testing"),
        ("medium", 4, 1000, "1m", "Medium load for staging"),
        ("heavy", 8, 2000, "2m", "Heavy load for production"),
        ("nuclear", 16, 5000, "30s", "Extreme load (use with caution)"),
    ]
    
    for preset in presets:
        table.add_row(*map(str, preset))
    
    console.print(table)

def main():
    app()

if __name__ == "__main__":
    main()