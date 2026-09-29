from __future__ import annotations

import json
import math
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()
LOG_PATH = Path("data/logs.jsonl")


def _percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    values_sorted = sorted(values)
    k = (len(values_sorted) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(values_sorted[int(k)])
    d0 = values_sorted[int(f)] * (c - k)
    d1 = values_sorted[int(c)] * (k - f)
    return float(round(d0 + d1, 2))


@router.get("/api/dashboard-data")
async def get_dashboard_data() -> dict[str, Any]:
    if not LOG_PATH.exists():
        return {"error": "logs.jsonl not found", "empty": True}

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=60)

    records: list[dict[str, Any]] = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
            ts_str = rec.get("ts")
            if ts_str:
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                if ts >= cutoff:
                    records.append(rec)
            else:
                records.append(rec)
        except Exception:
            continue

    req_received = [r for r in records if r.get("event") == "request_received"]
    req_sent = [r for r in records if r.get("event") == "response_sent"]
    req_failed = [r for r in records if r.get("event") == "request_failed"]

    # 1. Latency
    latencies = [float(r["latency_ms"]) for r in req_sent if "latency_ms" in r]
    ttfts = [float(r["ttft_ms"]) for r in req_sent if "ttft_ms" in r]
    p50 = _percentile(latencies, 50)
    p95 = _percentile(latencies, 95)
    p99 = _percentile(latencies, 99)
    ttft_p95 = _percentile(ttfts, 95)

    # 2. Traffic
    traffic_count = len(req_received)
    # Rate per minute across 60m window (or active minutes)
    active_minutes = max(1.0, min(60.0, (now - cutoff).total_seconds() / 60.0))
    rate_per_min = round(traffic_count / active_minutes, 2)

    # 3. Errors
    total_reqs = traffic_count if traffic_count > 0 else (len(req_sent) + len(req_failed))
    error_count = len(req_failed)
    error_rate_pct = round((error_count / total_reqs * 100) if total_reqs > 0 else 0.0, 2)
    
    error_breakdown: dict[str, int] = {}
    for r in req_failed:
        etype = r.get("error_type", "UnknownError")
        error_breakdown[etype] = error_breakdown.get(etype, 0) + 1

    tool_calls = [r for r in records if r.get("tool_name") is not None]
    tool_successes = [r for r in tool_calls if r.get("tool_success") is True]
    tool_success_rate_pct = round(
        (len(tool_successes) / len(tool_calls) * 100) if tool_calls else 100.0, 2
    )

    # 4. Cost
    costs = [float(r.get("cost_usd", 0.0)) for r in req_sent]
    total_cost = round(sum(costs), 5)

    # 5. Tokens
    tokens_in = sum(int(r.get("tokens_in", 0)) for r in req_sent)
    tokens_out = sum(int(r.get("tokens_out", 0)) for r in req_sent)
    total_tokens = tokens_in + tokens_out

    # 6. Quality
    qualities = [float(r.get("quality_score", 0.0)) for r in req_sent if "quality_score" in r]
    mean_quality = round(sum(qualities) / len(qualities), 2) if qualities else 0.0

    return {
        "time_window_minutes": 60,
        "records_count": len(records),
        "latency": {
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "ttft_p95": ttft_p95,
            "unit": "ms",
            "threshold_p95": 3000,
            "status": "PASS" if p95 <= 3000 else "ALERT",
        },
        "traffic": {
            "count": traffic_count,
            "rate_per_minute": rate_per_min,
            "unit": "requests_per_minute",
            "threshold_rate": 1,
            "status": "PASS" if traffic_count >= 1 else "IDLE",
        },
        "errors": {
            "error_rate_pct": error_rate_pct,
            "error_breakdown": error_breakdown,
            "tool_success_rate_pct": tool_success_rate_pct,
            "unit": "percent",
            "threshold_error_rate": 2.0,
            "status": "PASS" if error_rate_pct <= 2.0 else "ALERT",
        },
        "cost": {
            "total_usd": total_cost,
            "unit": "USD",
            "threshold_total": 2.50,
            "status": "PASS" if total_cost <= 2.50 else "ALERT",
        },
        "tokens": {
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "total_tokens": total_tokens,
            "unit": "tokens",
            "threshold_tokens": 50000,
            "status": "PASS" if total_tokens <= 50000 else "ALERT",
        },
        "quality": {
            "mean_quality_score": mean_quality,
            "unit": "score_0_to_1",
            "threshold_mean": 0.75,
            "status": "PASS" if mean_quality >= 0.75 else "ALERT",
        },
    }


DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>K4-L3A Day 13 Monitoring & LLMOps Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #0a0e17;
      --bg-card: rgba(18, 24, 38, 0.85);
      --border-color: rgba(56, 75, 112, 0.35);
      --text-main: #f0f4fc;
      --text-muted: #8e9bb2;
      --accent-cyan: #00d2ff;
      --accent-blue: #3a7bd5;
      --color-pass: #00e676;
      --color-alert: #ff1744;
      --color-warning: #ffab00;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Outfit', sans-serif;
      background: radial-gradient(circle at 10% 20%, #0d1527 0%, #060911 90%);
      color: var(--text-main);
      min-height: 100vh;
      padding: 24px;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border-color);
    }
    .header-left h1 {
      font-size: 24px;
      font-weight: 700;
      background: linear-gradient(135deg, #00d2ff, #7f53ac);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .header-left p {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 4px;
    }
    .header-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .badge {
      background: rgba(0, 210, 255, 0.1);
      border: 1px solid rgba(0, 210, 255, 0.3);
      color: var(--accent-cyan);
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-family: 'JetBrains Mono', monospace;
    }
    .btn-refresh {
      background: linear-gradient(135deg, #00d2ff, #3a7bd5);
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 13px;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .btn-refresh:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
    }
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 20px;
      backdrop-filter: blur(10px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 16px;
    }
    .card-title {
      font-size: 16px;
      font-weight: 600;
      color: var(--text-main);
    }
    .card-subtitle {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }
    .status-tag {
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 12px;
      font-family: 'JetBrains Mono', monospace;
    }
    .status-PASS { background: rgba(0, 230, 118, 0.15); color: var(--color-pass); border: 1px solid var(--color-pass); }
    .status-ALERT { background: rgba(255, 23, 68, 0.15); color: var(--color-alert); border: 1px solid var(--color-alert); }
    .status-IDLE { background: rgba(255, 171, 0, 0.15); color: var(--color-warning); border: 1px solid var(--color-warning); }
    .stat-row {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin: 12px 0;
    }
    .stat-box {
      background: rgba(255, 255, 255, 0.03);
      padding: 10px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stat-label {
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .stat-val {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      margin-top: 4px;
    }
    .threshold-bar {
      margin-top: 14px;
      padding-top: 10px;
      border-top: 1px dashed rgba(255, 255, 255, 0.1);
      font-size: 12px;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .threshold-val {
      color: var(--accent-cyan);
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <header>
    <div class="header-left">
      <h1>K4-L3A Day 13 Monitoring & LLMOps Dashboard</h1>
      <p>Hệ thống giám sát SLA/SLO runtime theo hợp đồng config/dashboard.yaml</p>
    </div>
    <div class="header-right">
      <div class="badge">Time Range: 60m</div>
      <div class="badge" id="refresh-badge">Refresh: 30s</div>
      <button class="btn-refresh" onclick="fetchData()">Làm mới</button>
    </div>
  </header>

  <main class="grid">
    <!-- Panel 1: Latency -->
    <div class="card" id="card-latency">
      <div class="card-head">
        <div>
          <div class="card-title">1. Latency percentiles and TTFT</div>
          <div class="card-subtitle">Source: response_sent.latency_ms / ttft_ms</div>
        </div>
        <span class="status-tag" id="status-latency">LOADING</span>
      </div>
      <div class="stat-row">
        <div class="stat-box">
          <div class="stat-label">P50 Latency</div>
          <div class="stat-val" id="lat-p50">--</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">P95 Latency</div>
          <div class="stat-val" id="lat-p95">--</div>
        </div>
      </div>
      <div class="stat-row">
        <div class="stat-box">
          <div class="stat-label">P99 Latency</div>
          <div class="stat-val" id="lat-p99">--</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">TTFT P95</div>
          <div class="stat-val" id="lat-ttft">--</div>
        </div>
      </div>
      <div class="threshold-bar">
        <span>SLO Threshold:</span>
        <span class="threshold-val">P95 &le; 3000 ms</span>
      </div>
    </div>

    <!-- Panel 2: Traffic -->
    <div class="card" id="card-traffic">
      <div class="card-head">
        <div>
          <div class="card-title">2. Request traffic</div>
          <div class="card-subtitle">Source: request_received events</div>
        </div>
        <span class="status-tag" id="status-traffic">LOADING</span>
      </div>
      <div class="stat-row">
        <div class="stat-box">
          <div class="stat-label">Total Requests</div>
          <div class="stat-val" id="traffic-total">--</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Rate / Minute</div>
          <div class="stat-val" id="traffic-rate">--</div>
        </div>
      </div>
      <div class="threshold-bar">
        <span>Traffic Threshold:</span>
        <span class="threshold-val">&ge; 1 req/min</span>
      </div>
    </div>

    <!-- Panel 3: Errors -->
    <div class="card" id="card-errors">
      <div class="card-head">
        <div>
          <div class="card-title">3. Error rate and retrieval success</div>
          <div class="card-subtitle">Source: request_failed & tool_success</div>
        </div>
        <span class="status-tag" id="status-errors">LOADING</span>
      </div>
      <div class="stat-row">
        <div class="stat-box">
          <div class="stat-label">Error Rate</div>
          <div class="stat-val" id="err-rate">--</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Retrieval Success</div>
          <div class="stat-val" id="retrieval-rate">--</div>
        </div>
      </div>
      <div class="threshold-bar">
        <span>Guardrail Threshold:</span>
        <span class="threshold-val">Error &le; 2%, Success &ge; 90%</span>
      </div>
    </div>

    <!-- Panel 4: Cost -->
    <div class="card" id="card-cost">
      <div class="card-head">
        <div>
          <div class="card-title">4. Cost over time</div>
          <div class="card-subtitle">Source: response_sent.cost_usd</div>
        </div>
        <span class="status-tag" id="status-cost">LOADING</span>
      </div>
      <div class="stat-row">
        <div class="stat-box">
          <div class="stat-label">Total Window Cost</div>
          <div class="stat-val" id="cost-total">--</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Unit</div>
          <div class="stat-val" style="font-size:16px;">USD ($)</div>
        </div>
      </div>
      <div class="threshold-bar">
        <span>Cost Threshold:</span>
        <span class="threshold-val">Total &le; $2.50 USD</span>
      </div>
    </div>

    <!-- Panel 5: Tokens -->
    <div class="card" id="card-tokens">
      <div class="card-head">
        <div>
          <div class="card-title">5. Input and output tokens</div>
          <div class="card-subtitle">Source: tokens_in & tokens_out</div>
        </div>
        <span class="status-tag" id="status-tokens">LOADING</span>
      </div>
      <div class="stat-row">
        <div class="stat-box">
          <div class="stat-label">Input Tokens</div>
          <div class="stat-val" id="tok-in">--</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Output Tokens</div>
          <div class="stat-val" id="tok-out">--</div>
        </div>
      </div>
      <div class="threshold-bar">
        <span>Token Threshold:</span>
        <span class="threshold-val">Total &le; 50,000 tokens</span>
      </div>
    </div>

    <!-- Panel 6: Quality -->
    <div class="card" id="card-quality">
      <div class="card-head">
        <div>
          <div class="card-title">6. Quality proxy</div>
          <div class="card-subtitle">Source: response_sent.quality_score</div>
        </div>
        <span class="status-tag" id="status-quality">LOADING</span>
      </div>
      <div class="stat-row">
        <div class="stat-box">
          <div class="stat-label">Mean Quality Score</div>
          <div class="stat-val" id="quality-mean">--</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Score Range</div>
          <div class="stat-val" style="font-size:16px;">0.00 &ndash; 1.00</div>
        </div>
      </div>
      <div class="threshold-bar">
        <span>Quality Threshold:</span>
        <span class="threshold-val">Mean &ge; 0.75</span>
      </div>
    </div>
  </main>

  <script>
    async function fetchData() {
      try {
        const res = await fetch('/api/dashboard-data');
        const d = await res.json();
        if (d.empty) return;

        // 1. Latency
        document.getElementById('lat-p50').textContent = d.latency.p50 + ' ms';
        document.getElementById('lat-p95').textContent = d.latency.p95 + ' ms';
        document.getElementById('lat-p99').textContent = d.latency.p99 + ' ms';
        document.getElementById('lat-ttft').textContent = d.latency.ttft_p95 + ' ms';
        setTag('status-latency', d.latency.status);

        // 2. Traffic
        document.getElementById('traffic-total').textContent = d.traffic.count;
        document.getElementById('traffic-rate').textContent = d.traffic.rate_per_minute + ' /min';
        setTag('status-traffic', d.traffic.status);

        // 3. Errors
        document.getElementById('err-rate').textContent = d.errors.error_rate_pct + ' %';
        document.getElementById('retrieval-rate').textContent = d.errors.tool_success_rate_pct + ' %';
        setTag('status-errors', d.errors.status);

        // 4. Cost
        document.getElementById('cost-total').textContent = '$' + d.cost.total_usd.toFixed(4);
        setTag('status-cost', d.cost.status);

        // 5. Tokens
        document.getElementById('tok-in').textContent = d.tokens.tokens_in.toLocaleString();
        document.getElementById('tok-out').textContent = d.tokens.tokens_out.toLocaleString();
        setTag('status-tokens', d.tokens.status);

        // 6. Quality
        document.getElementById('quality-mean').textContent = d.quality.mean_quality_score.toFixed(2);
        setTag('status-quality', d.quality.status);
      } catch (err) {
        console.error('Fetch error:', err);
      }
    }

    function setTag(id, status) {
      const el = document.getElementById(id);
      el.textContent = status;
      el.className = 'status-tag status-' + status;
    }

    fetchData();
    setInterval(fetchData, 30000);
  </script>
</body>
</html>
"""


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page() -> str:
    return DASHBOARD_HTML
