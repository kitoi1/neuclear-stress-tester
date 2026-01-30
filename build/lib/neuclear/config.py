"""
Configuration management
"""

import re
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

@dataclass
class Config:
    """Configuration for stress tests"""
    target_url: str
    processes: int = 4
    rate: int = 1000  # Requests per second per process
    duration: str = "30s"  # Can be "30s", "1m", "2h", etc.
    output_file: str = "report.json"
    timeout: int = 30  # Seconds
    headers: Optional[dict] = None
    payload_file: Optional[str] = None
    
    def __post_init__(self):
        # Validate URL format
        if not re.match(r'^https?://', self.target_url):
            raise ValueError("URL must start with http:// or https://")
        
        # Validate numeric inputs
        if self.processes <= 0:
            raise ValueError("Processes must be positive")
        
        if self.rate <= 0:
            raise ValueError("Rate must be positive")
        
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
        
        # Parse duration
        if not re.match(r'^\d+[smh]$', self.duration):
            raise ValueError("Duration must be in format like '30s', '1m', '2h'")
    
    @property
    def duration_seconds(self) -> float:
        """Convert duration string to seconds"""
        match = re.match(r'^(\d+)([smh])$', self.duration)
        if not match:
            return 30.0  # Default
        
        value, unit = match.groups()
        value = int(value)
        
        if unit == 's':
            return value
        elif unit == 'm':
            return value * 60
        elif unit == 'h':
            return value * 3600
        else:
            return 30.0
    
    @property
    def total_rate(self) -> int:
        """Total requests per second across all processes"""
        return self.processes * self.rate
    
    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            "target_url": self.target_url,
            "processes": self.processes,
            "rate": self.rate,
            "total_rate": self.total_rate,
            "duration": self.duration,
            "duration_seconds": self.duration_seconds,
            "output_file": self.output_file,
            "timeout": self.timeout,
        }
    
    def save(self, filename: str):
        """Save config to file"""
        import json
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, filename: str) -> 'Config':
        """Load config from file"""
        import json
        with open(filename, 'r') as f:
            data = json.load(f)
        
        return cls(
            target_url=data["target_url"],
            processes=data.get("processes", 4),
            rate=data.get("rate", 1000),
            duration=data.get("duration", "30s"),
            output_file=data.get("output_file", "report.json"),
            timeout=data.get("timeout", 30),
        )

def create_default_config() -> Config:
    """Create a default configuration"""
    return Config(
        target_url="http://localhost:8080",
        processes=4,
        rate=1000,
        duration="30s",
        output_file="stress_test_report.json",
        timeout=30,
    )