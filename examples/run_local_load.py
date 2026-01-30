#!/usr/bin/env python3
"""
Example: Run local load test
"""

import asyncio
import time
from neuclear import StressTest
from neuclear.config import Config

async def main():
    """Run a local load test example"""
    print("🚀 Starting local load test example...")
    
    # Configuration for local testing
    config = Config(
        target_url="http://localhost:8080",
        processes=2,
        rate=100,
        duration="10s",
        output_file="local_test_report.json",
    )
    
    print(f"Testing: {config.target_url}")
    print(f"Processes: {config.processes}")
    print(f"Rate: {config.rate} RPS/process")
    print(f"Total Rate: {config.total_rate} RPS")
    print(f"Duration: {config.duration}")
    
    # Run the test
    stress_test = StressTest(config)
    results = await stress_test.run()
    
    # Print results
    print("\n📊 Test Results:")
    print(f"Total Requests: {results.total_requests}")
    print(f"Successful: {results.successful}")
    print(f"Failed: {results.failed}")
    print(f"Success Rate: {results.success_rate:.2f}%")
    print(f"Average Latency: {results.avg_latency:.2f}ms")
    print(f"Requests/sec: {results.rps:.2f}")
    
    # Save report
    results.save_report(config.output_file)
    print(f"\n✅ Report saved to: {config.output_file}")

if __name__ == "__main__":
    asyncio.run(main())