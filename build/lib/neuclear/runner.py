"""
Test runner and worker orchestration
"""

import asyncio
import multiprocessing
from typing import List, Optional
from concurrent.futures import ProcessPoolExecutor
import time
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.live import Live
from rich.table import Table

from .config import Config
from .core import StressTest, TestResult
from .utils import print_banner, get_system_info

class TestRunner:
    """Orchestrates multiple stress tests"""
    
    def __init__(self, config: Config):
        self.config = config
        self.results: List[TestResult] = []
        self.progress = None
    
    async def run_single_test(self, test_config: Config) -> TestResult:
        """Run a single stress test"""
        stress_test = StressTest(test_config)
        return await stress_test.run()
    
    def run_concurrent_tests(self, configs: List[Config]) -> List[TestResult]:
        """Run multiple tests concurrently"""
        async def run_all():
            tasks = [self.run_single_test(config) for config in configs]
            return await asyncio.gather(*tasks)
        
        return asyncio.run(run_all())
    
    def run_with_progress(self) -> TestResult:
        """Run test with progress bar"""
        print_banner()
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ) as progress:
            
            task = progress.add_task(
                f"[cyan]Testing {self.config.target_url}...",
                total=self.config.duration_seconds
            )
            
            async def run_with_update():
                stress_test = StressTest(self.config)
                start_time = time.time()
                
                # Run test in background
                test_task = asyncio.create_task(stress_test.run())
                
                # Update progress while test runs
                while not test_task.done():
                    elapsed = time.time() - start_time
                    progress.update(task, completed=min(elapsed, self.config.duration_seconds))
                    await asyncio.sleep(0.1)
                
                return await test_task
            
            result = asyncio.run(run_with_update())
            progress.update(task, completed=self.config.duration_seconds)
        
        return result
    
    def monitor_system(self, interval: float = 1.0):
        """Monitor system resources during test"""
        table = Table(title="System Monitoring")
        table.add_column("Metric")
        table.add_column("Value")
        
        with Live(table, refresh_per_second=4) as live:
            try:
                while True:
                    info = get_system_info()
                    
                    table.rows = []
                    table.add_row("CPU Count", str(info["cpu_count"]))
                    table.add_row("CPU Usage", f"{info['cpu_percent']:.1f}%")
                    table.add_row("Memory Available", f"{info['memory_available'] / 1e9:.2f} GB")
                    table.add_row("Network Connections", str(info["network_connections"]))
                    
                    live.update(table)
                    time.sleep(interval)
            except KeyboardInterrupt:
                pass

def create_runner_from_config(config: Config) -> TestRunner:
    """Create a runner from configuration"""
    return TestRunner(config)