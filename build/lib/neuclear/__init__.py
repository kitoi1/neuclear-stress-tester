"""
Nuclear Stress Tester - High-performance load testing tool
"""

__version__ = "4.0.0"
__author__ = "Kasau"
__description__ = "Ultimate Nuclear Stress Tester for Developers"

from .cli import main
from .core import StressTest
from .config import Config

__all__ = ["main", "StressTest", "Config"]