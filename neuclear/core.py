"""
Core stress testing logic
"""

import asyncio
import aiohttp
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import statistics
from concurrent.futures import ProcessPoolExecutor
import json
from rich import print
from .config import Config

@dataclass
class TestResult:
    """Container for test results"""
    total_requests: int = 0
    successful: int = 0
    failed: int = 0
    status_codes: Dict[int, int] = None
    latencies: List[float] = None
    start_time: float = 0
    end_time: float = 0
    
    def __post_init__(self):
        if self.status_codes is None:
            self.status_codes = {}
        if self.latencies is None:
            self.latencies = []
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return (self.successful / self.total_requests) * 100
    
    @property
    def avg_latency(self) -> float:
        if not self.latencies:
            return 0.0
        return statistics.mean(self.latencies)
    
    @property
    def p95_latency(self) -> float:
        if not self.latencies:
            return 0.0
        return statistics.quantiles(self.latencies, n=100)[94]
    
    @property
    def p99_latency(self) -> float:
        if not self.latencies:
            return 0.0
        return statistics.quantiles(self.latencies, n=100)[98]
    
    @property
    def rps(self) -> float:
        duration = self.end_time - self.start_time
        if duration == 0:
            return 0.0
        return self.total_requests / duration
    
    def save_report(self, filename: str):
        """Save report to JSON file"""
        report = {
            "total_requests": self.total_requests,
            "successful": self.successful,
            "failed": self.failed,
            "success_rate": self.success_rate,
            "avg_latency": self.avg_latency,
            "p95_latency": self.p95_latency,
            "p99_latency": self.p99_latency,
            "requests_per_second": self.rps,
            "status_codes": self.status_codes,
            "duration_seconds": self.end_time - self.start_time,
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

class StressTest:
    """Main stress test orchestrator"""
    
    def __init__(self, config: Config):
        self.config = config
        self.results = TestResult()
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def make_request(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Make a single HTTP request"""
        start_time = time.time()
        
        try:
            async with session.get(self.config.target_url) as response:
                latency = (time.time() - start_time) * 1000  # Convert to ms
                
                return {
                    "success": response.status < 400,
                    "status_code": response.status,
                    "latency": latency,
                    "error": None,
                }
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return {
                "success": False,
                "status_code": 0,
                "latency": latency,
                "error": str(e),
            }
    
    async def worker(self, worker_id: int, rate: int, duration: float):
        """Worker that makes requests at specified rate"""
        requests_per_second = rate
        delay = 1.0 / requests_per_second
        
        end_time = time.time() + duration
        local_results = TestResult()
        
        connector = aiohttp.TCPConnector(limit=0)  # No connection limit
        async with aiohttp.ClientSession(connector=connector) as session:
            while time.time() < end_time:
                start_request = time.time()
                
                result = await self.make_request(session)
                
                # Update local results
                local_results.total_requests += 1
                if result["success"]:
                    local_results.successful += 1
                    local_results.latencies.append(result["latency"])
                    status_code = result["status_code"]
                    local_results.status_codes[status_code] = local_results.status_codes.get(status_code, 0) + 1
                else:
                    local_results.failed += 1
                
                # Calculate time to wait to maintain rate
                request_time = time.time() - start_request
                sleep_time = max(0, delay - request_time)
                
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
        
        return local_results
    
    async def run(self) -> TestResult:
        """Run the stress test"""
        print(f"[cyan]Starting stress test with {self.config.processes} workers...[/cyan]")
        
        self.results.start_time = time.time()
        
        # Create tasks for each worker
        tasks = []
        for i in range(self.config.processes):
            task = self.worker(i, self.config.rate, self.config.duration_seconds)
            tasks.append(task)
        
        # Run all workers concurrently
        worker_results = await asyncio.gather(*tasks)
        
        # Aggregate results
        for result in worker_results:
            self.results.total_requests += result.total_requests
            self.results.successful += result.successful
            self.results.failed += result.failed
            self.results.latencies.extend(result.latencies)
            
            for status_code, count in result.status_codes.items():
                self.results.status_codes[status_code] = self.results.status_codes.get(status_code, 0) + count
        
        self.results.end_time = time.time()
        
        return self.results