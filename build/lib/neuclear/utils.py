"""
Utility functions
"""

import re
import time
from typing import Optional, Tuple
import asyncio
import socket
import psutil
from rich.console import Console

console = Console()

def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = re.compile(
        r'^(https?|ftp)://'  # Protocol
        r'([A-Za-z0-9\-]+\.)+[A-Za-z]{2,}'  # Domain
        r'(:\d+)?'  # Port
        r'(/.*)?$'  # Path
    )
    return bool(pattern.match(url))

def format_duration(seconds: float) -> str:
    """Format seconds into human readable duration"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def parse_duration(duration_str: str) -> float:
    """Parse duration string to seconds"""
    match = re.match(r'^(\d+)([smh])$', duration_str)
    if not match:
        raise ValueError(f"Invalid duration format: {duration_str}")
    
    value, unit = match.groups()
    value = int(value)
    
    multipliers = {
        's': 1,
        'm': 60,
        'h': 3600,
    }
    
    return value * multipliers[unit]

def get_system_info() -> dict:
    """Get system information for monitoring"""
    return {
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_total": psutil.virtual_memory().total,
        "memory_available": psutil.virtual_memory().available,
        "network_connections": len(psutil.net_connections()),
    }

def is_port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    """Check if a port is open on a host"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    except Exception:
        return False

async def async_is_port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    """Async version of port checking"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except (asyncio.TimeoutError, ConnectionRefusedError):
        return False
    except Exception:
        return False

def calculate_statistics(data: list) -> dict:
    """Calculate statistics from a list of numbers"""
    if not data:
        return {
            "mean": 0,
            "median": 0,
            "min": 0,
            "max": 0,
            "std": 0,
            "count": 0,
        }
    
    import statistics
    
    return {
        "mean": statistics.mean(data),
        "median": statistics.median(data),
        "min": min(data),
        "max": max(data),
        "std": statistics.stdev(data) if len(data) > 1 else 0,
        "count": len(data),
    }

def print_banner():
    """Print the ASCII art banner"""
    banner = """
  _   _ _   _ _ _ _   _           _____ _                 _____         _            
 | | | | |_(_) (_) |_(_)_ __ ___ |_   _| |__   ___ _ __  |_   _| __ ___| |_ ___ _ __ 
 | | | | __| | | | __| | '_ ` _ \  | | | '_ \ / _ \ '__|   | | | '__/ _ \ __/ _ \ '__|
 | |_| | |_| | | | |_| | | | | | | | | | | | |  __/ |      | | | | |  __/ ||  __/ |   
  \___/ \__|_|_|_|\__|_|_| |_| |_| |_| |_| |_|\___|_|      |_| |_|  \___|\__\___|_|   
    
    💣 Ultimate Nuclear Stress Tester v4.0
    """
    console.print(f"[magenta]{banner}[/magenta]")