# 💣 Nuclear Stress Tester  
**Ultimate Load Testing Tool for Websites & APIs**

![Version](https://img.shields.io/badge/version-4.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Stars](https://img.shields.io/github/stars/kitoi1/neuclear-stress-tester?style=social)
![Forks](https://img.shields.io/github/forks/kitoi1/neuclear-stress-tester?style=social)

**Nuclear Stress Tester** is a powerful load-testing weapon for developers who want to know **exactly how much traffic their servers can handle before they break**.

Test websites and APIs under extreme load **before real users do**.

---

## 🎯 What Does This Tool Do?

Imagine launching a new website or API.

You *think* it can handle traffic…  
But what happens when **10,000 users hit it at the same time**?

**Nuclear Stress Tester answers that question safely and early.**

### In Simple Terms
- Simulates thousands of users hitting your site simultaneously
- Measures performance under extreme conditions
- Finds breaking points before production incidents
- Generates clear, actionable performance reports

---

## 🚀 Quick Start (60 Seconds)

### 1️⃣ Install the Tool

```bash
# Clone the repository
git clone https://github.com/kitoi1/neuclear-stress-tester.git
cd neuclear-stress-tester

# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate       # Windows

# Install
pip install -e . 
```
 

### 2️⃣ Run Your First Test

```bash 
# Safe public test endpoint
neuclear test https://httpbin.org/get --processes 2 --rate 5 --duration 10s

# Example output:
	💣 Nuclear Stress Tester v4.0
Target: https://httpbin.org/get
Processes: 2
Rate: 5 RPS/process (Total: 10 RPS)
Duration: 10s

[████████████████████████████████████████] 100%
Test complete!

# 📊 Results Summary

┌─────────────────┬─────────┐
│ Metric          │ Value   │
├─────────────────┼─────────┤
│ Total Requests  │ 100     │
│ Successful      │ 100     │
│ Failed          │ 0       │
│ Success Rate    │ 100.00% │
│ Average Latency │ 150ms   │
│ Requests/sec    │ 10.0    │
└─────────────────┴─────────┘

🎉 Congrats! You just ran your first stress test.
```

📖 Beginner’s Guide
What Is Load Testing?
### Scenario
Think of it like stress-testing a bridge:
How many cars (requests) can it carry?
When does it collapse?
How bad is rush hour?
When Should You Use This Tool?

### Why Test
New website launch	Avoid launch-day crashes
Promotions & sales	Handle traffic spikes
New feature deployment	Catch performance regressions
Choosing hosting plans	Know what specs you actually need
Debugging slowness	Identify bottlenecks

## Understanding the Basics
```bash
neuclear test https://example.com --processes 2 --rate 5 --duration 10s
```
## Part	  										## Meaning
```bash
neuclear test								Run a stress test
URL											Target website or API
--processes 2								Number of workers
--rate 5									Requests per second per worker
--duration 10s								Test duration


Total Load	10 RPS (2 × 5)
🔧 Installation Options
Option 1: Virtual Environment (Recommended)
```

### Isolated, clean, and safe — use Quick Start above.

## Option 2: Global Install

```bash
pip install git+https://github.com/kitoi1/neuclear-stress-tester.git
neuclear --help
```

## Option 3: Docker

# 🚧 Coming soon

### 🎮 Interactive Tutorial

## Lesson 1: Safe Public Testing
```bash
neuclear test https://httpbin.org/get
neuclear test https://httpbin.org/get --processes 4 --rate 10 --duration 30s
neuclear test https://httpbin.org/delay/2
```

## Lesson 2: Test Your Own Server

# Terminal 1
```bash
python3 -m http.server 8080
```

# Terminal 2
```bash
neuclear test http://localhost:8080 --processes 2 --rate 10 --duration 15s
```

## Lesson 3: Reading Results

# Metric						Meaning						Good Value

Total Requests			Requests sent				Depends
Successful				Completed requests			High
Failed					Errors						Low
Success 				Rate						Reliability	95%+
Avg Latency				Response time				< 500ms
Requests/sec			Throughput					Higher


### 📊 Real-World Examples

## Blog Launch
```bash
neuclear test https://yourblog.com --processes 10 --rate 10 --duration 1m
```

## API Rate Limit Test
```bash
neuclear test https://api.yourservice.com --processes 1 --rate 17 --duration 1m
```

## Find Breaking Point
```bash
neuclear test https://yoursite.com --processes 2 --rate 10 --duration 30s
neuclear test https://yoursite.com --processes 4 --rate 25 --duration 30s
neuclear test https://yoursite.com --processes 8 --rate 50 --duration 30s
```

### ⚙️ Configuration Options

# Parameter		   Short		  Description		  Default
--processes			-p			Parallel workers		4
--rate				-r			RPS per worker			1000
--duration			-d			Test duration			30s
--output			-o			Save JSON reports		report.json
--quiet				-q			Minimal output			False

# 🚨 Safety Warnings (READ THIS)

### ⚠️ DO NOT test servers you don’t own or have permission to test

❌ Illegal in many regions
❌ Can get you banned
❌ May be treated as an attack

## ✅ Safe Targets
```bash
https://httpbin.org
https://jsonplaceholder.typicode.com
```
