"""Analyze synthetic cellular network telemetry."""
import argparse
import csv
import json
from collections import defaultdict

def analyze(rows, latency_limit=120, loss_limit=2.0, uptime_limit=99.0):
    sites = defaultdict(list)
    for row in rows:
        site = row["site_id"].strip()
        if not site:
            raise ValueError("site_id cannot be empty")
        metrics = {k: float(row[k]) for k in ("latency_ms", "packet_loss_pct", "uptime_pct")}
        if not (0 <= metrics["packet_loss_pct"] <= 100 and 0 <= metrics["uptime_pct"] <= 100 and metrics["latency_ms"] >= 0):
            raise ValueError(f"Invalid metric for {site}")
        sites[site].append(metrics)
    report = {}
    for site, records in sorted(sites.items()):
        avg = {key: round(sum(r[key] for r in records) / len(records), 2) for key in records[0]}
        alerts = []
        if avg["latency_ms"] > latency_limit: alerts.append("HIGH_LATENCY")
        if avg["packet_loss_pct"] > loss_limit: alerts.append("PACKET_LOSS")
        if avg["uptime_pct"] < uptime_limit: alerts.append("LOW_UPTIME")
        report[site] = {"samples": len(records), "averages": avg, "alerts": alerts, "status": "DEGRADED" if alerts else "HEALTHY"}
    return report

def main():
    parser = argparse.ArgumentParser(description="Analyze synthetic network telemetry")
    parser.add_argument("--input", default="sample_metrics.csv")
    args = parser.parse_args()
    with open(args.input, newline="", encoding="utf-8") as handle:
        report = analyze(csv.DictReader(handle))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
