"""
Generate real-time executive metrics (fact_realtime_metrics).
Hourly snapshots over 7 days simulating live business + system telemetry.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'realtime')


def generate_realtime(hours: int = 168):
    """Generate hourly metric snapshots (default: 7 days)."""
    print(f"  Generating {hours} hourly real-time metric snapshots...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    base = datetime(2026, 2, 9, 0, 0, 0)
    records = []

    for h in range(hours):
        ts = base - timedelta(hours=hours - 1 - h)
        hour = ts.hour
        mult = 0.3 if hour < 6 else (1.5 if 9 <= hour <= 17 else 0.6)

        records.append({
            'timestamp': ts.isoformat(),
            'hour_label': ts.strftime('%m/%d %H:00'),
            'day': ts.strftime('%a'),
            'active_users': int(random.gauss(450, 80) * mult),
            'page_views': int(random.gauss(2200, 400) * mult),
            'api_calls': int(random.gauss(15000, 3000) * mult),
            'avg_response_ms': round(random.gauss(180, 40), 1),
            'error_rate_pct': round(max(0, random.gauss(0.8, 0.3)), 2),
            'pipeline_value': round(random.gauss(45, 8) * 1e6, 0),
            'deals_closed_today': random.randint(0, 5) if 9 <= hour <= 17 else 0,
            'revenue_today': round(random.gauss(8, 3) * 1e6, 0) if 9 <= hour <= 17 else 0,
            'new_leads': random.randint(0, 12) if 9 <= hour <= 17 else random.randint(0, 3),
            'support_tickets_open': random.randint(15, 45),
            'avg_csat': round(random.gauss(4.2, 0.3), 2),
            'uptime_pct': round(min(100, random.gauss(99.95, 0.03)), 3),
            'etl_jobs_running': random.randint(0, 8),
            'dq_pass_rate': round(min(100, random.gauss(97.5, 1.2)), 1),
        })

    df = pd.DataFrame(records)
    df.to_csv(os.path.join(OUTPUT_DIR, 'fact_realtime_metrics.csv'), index=False)
    print(f"    Snapshots: {len(df)} | Avg users: {df['active_users'].mean():.0f}")
    return df
