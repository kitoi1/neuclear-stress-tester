# Changelog

All notable changes to Nuclear Stress Tester will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2025-04-28

### Added
- Complete Python package structure
- New CLI interface using Typer
- Asynchronous architecture with aiohttp
- Rich console output and progress bars
- Configuration management system
- System resource monitoring
- Comprehensive test suite structure
- Pre-commit hooks for code quality
- GitHub Actions workflows

### Changed
- Rewritten from Bash script to Python package
- Improved error handling and validation
- Enhanced reporting capabilities
- Better performance with async/await
- Modular architecture for extensibility

### Deprecated
- Original Bash script (moved to examples/)

## [Unreleased]

### Planned
- Web dashboard for real-time monitoring
- Distributed testing across multiple machines
- More protocol support (WebSocket, gRPC)
- Integration with monitoring tools
- Plugin system for custom metrics