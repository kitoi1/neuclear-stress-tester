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
    processes: int = typer.Option(4, "--processes", "-p", help="Number of processes (1-100)"),
    rate: int = typer.Option(1000, "--rate", "-r", help="Requests per second per process (1-10000)"),
    duration: str = typer.Option("30s", "--duration", "-d", help="Test duration (e.g., 30s, 1m, 2h)"),
    output: str = typer.Option("report.json", "--output", "-o", help="Output report file"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress verbose output"),
):
    """
    Run a stress test against a target URL
    """
    # Import here to avoid circular imports
    from neuclear.utils import validate_url_simple
    from neuclear.core import StressTest
    from neuclear.config import Config
    
    # Validate inputs
    if not validate_url_simple(url):
        console.print("[red]Error: Invalid URL format. Include http:// or https://[/red]")
        raise typer.Exit(1)
    
    # SANITY CHECKS - ADD THESE!
    if processes <= 0:
        console.print("[red]Error: Number of processes must be positive[/red]")
        raise typer.Exit(1)
    
    if processes > 100:
        console.print(f"[yellow]Warning: {processes} processes is too high. Limiting to 100.[/yellow]")
        processes = 100
    
    if rate <= 0:
        console.print("[red]Error: Rate must be positive[/red]")
        raise typer.Exit(1)
    
    if rate > 10000:
        console.print(f"[yellow]Warning: {rate} RPS per process is too high. Limiting to 10,000.[/yellow]")
        rate = 10000
    
    # Calculate total rate
    total_rate = processes * rate
    
    if total_rate > 1000000:  # 1 million RPS max
        console.print(f"[red]Error: Total rate {total_rate} RPS exceeds maximum of 1,000,000 RPS[/red]")
        console.print("[yellow]Please reduce processes or rate.[/yellow]")
        raise typer.Exit(1)
    
    console.print(f"[bold magenta]💣 Nuclear Stress Tester v4.0[/bold magenta]")
    console.print(f"[cyan]Target:[/cyan] {url}")
    console.print(f"[cyan]Processes:[/cyan] {processes}")
    console.print(f"[cyan]Rate:[/cyan] {rate} RPS/process (Total: {total_rate} RPS)")
    console.print(f"[cyan]Duration:[/cyan] {duration}")
    
    # Warn if parameters are too high
    import psutil
    cpu_count = psutil.cpu_count()
    if processes > cpu_count * 4:
        console.print(f"[yellow]⚠️  Warning: You have {cpu_count} CPU cores but {processes} processes")
        console.print(f"   Consider using {cpu_count * 2} processes for optimal performance[/yellow]")
    
    # ... rest of the function

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