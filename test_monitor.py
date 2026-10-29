import csv
import io
import unittest
from monitor import analyze

class MonitorTests(unittest.TestCase):
    def test_degraded_site(self):
        rows = list(csv.DictReader(io.StringIO("site_id,latency_ms,packet_loss_pct,uptime_pct\nA,150,3,98\n")))
        self.assertEqual(analyze(rows)["A"]["status"], "DEGRADED")
        self.assertEqual(len(analyze(rows)["A"]["alerts"]), 3)

    def test_empty_input(self):
        self.assertEqual(analyze([]), {})

    def test_invalid_percent(self):
        with self.assertRaises(ValueError):
            analyze([{"site_id":"A","latency_ms":"10","packet_loss_pct":"101","uptime_pct":"99"}])
