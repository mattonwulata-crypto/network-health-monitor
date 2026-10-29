# Network Health Monitor

A Python CLI for analyzing simulated telecom network measurements. It flags high latency, packet loss, and low uptime, then summarizes reliability by cell site.

## Run
```bash
python monitor.py --input sample_metrics.csv
python -m unittest discover -s tests
```
Uses only Python's standard library. Data is synthetic; this is not connected to T-Mobile infrastructure.
