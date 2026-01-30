# Nuclear Stress Tester Documentation

Welcome to the Nuclear Stress Tester documentation!

## Overview

Nuclear Stress Tester is a high-performance load testing tool designed for developers who need to test the limits of their applications. It provides:

- **High concurrency** testing with async architecture
- **Detailed metrics** and reporting
- **Flexible configuration** options
- **Beautiful CLI interface** with rich output

## Quick Links

- [Installation Guide](installation.md)
- [Getting Started](getting-started.md)
- [Configuration Reference](configuration.md)
- [API Documentation](api.md)
- [Examples](examples.md)

## Features

### Performance
- Asynchronous architecture using asyncio
- Configurable worker processes
- Precise request timing
- Connection pooling

### Reporting
- Real-time progress tracking
- Detailed latency statistics (p50, p95, p99)
- Success/failure rates
- Status code distribution
- JSON report export

### Usability
- Intuitive CLI with helpful prompts
- Color-coded output
- Interactive mode
- Preset configurations

## Architecture

```mermaid
graph TD
    A[CLI Interface] --> B[Test Runner]
    B --> C[Worker Pool]
    C --> D[HTTP Client]
    D --> E[Target Server]
    C --> F[Metrics Collector]
    F --> G[Report Generator]
    G --> H[Console Output]
    G --> I[JSON Report]