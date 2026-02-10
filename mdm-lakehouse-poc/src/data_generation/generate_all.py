#!/usr/bin/env python3
"""
Master Data Generation Orchestrator
====================================
Generates the complete MDM Lakehouse dataset across all 11 tables.

Usage:
    python src/data_generation/generate_all.py

Output:
    data/bronze/      - Raw source extracts (SAP, Salesforce)
    data/gold/        - Star schema dimensions and facts
    data/mdm/         - MDM match pair results
    data/clickstream/ - Web analytics events
    data/pipeline/    - GTM sales deals
    data/fraud/       - Fraud detection alerts
    data/realtime/    - Executive metric snapshots
"""

import sys
import os
import time

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from generate_core_data import main as generate_core
from generate_clickstream import generate_clickstream
from generate_lifecycle import generate_lifecycle
from generate_pipeline import generate_pipeline
from generate_fraud import generate_fraud
from generate_realtime import generate_realtime

import pandas as pd


def main():
    start = time.time()

    print("=" * 70)
    print("  MDM LAKEHOUSE POC — FULL DATA GENERATION")
    print("  Idea to Display | Claude Opus 4.6 | Simultaneous")
    print("=" * 70)
    print()

    # ── Phase 1: Core data (Bronze → Gold + MDM) ──
    print("PHASE 1: Core Lakehouse Data")
    generate_core()
    print()

    # Load customer UIDs for downstream modules
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    customers_df = pd.read_csv(os.path.join(data_dir, 'gold', 'dim_customer.csv'))
    customer_uids = customers_df['customer_uid'].tolist()

    # ── Phase 2: Clickstream ──
    print("PHASE 2: Clickstream Data")
    generate_clickstream(customer_uids)
    print()

    # ── Phase 3: Customer Lifecycle ──
    print("PHASE 3: Customer Lifecycle")
    generate_lifecycle(customers_df)
    print()

    # ── Phase 4: GTM Pipeline ──
    print("PHASE 4: GTM Sales Pipeline")
    generate_pipeline(customer_uids)
    print()

    # ── Phase 5: Fraud Tracking ──
    print("PHASE 5: Fraud Detection")
    generate_fraud(customer_uids)
    print()

    # ── Phase 6: Real-Time Metrics ──
    print("PHASE 6: Real-Time Executive Metrics")
    generate_realtime()
    print()

    # ── Summary ──
    elapsed = time.time() - start
    print("=" * 70)
    print("  GENERATION COMPLETE")
    print(f"  Time: {elapsed:.1f}s")
    print()
    print("  Tables generated:")
    print("    dim_customer             500 golden records")
    print("    dim_product               80 products")
    print("    dim_customer_lifecycle   500 lifecycle records")
    print("    dim_date                 762 calendar days")
    print("    fact_sales             3,500 order transactions")
    print("    fact_interactions      6,000 customer touchpoints")
    print("    fact_clickstream      25,000 web events")
    print("    fact_pipeline          1,200 GTM deals")
    print("    fact_realtime_metrics    168 hourly snapshots")
    print("    fact_fraud_signals       450 fraud alerts")
    print("    mdm_match_pairs          200 candidate pairs")
    print("    ─────────────────────────────")
    print("    TOTAL                 36,650+ records")
    print("=" * 70)


if __name__ == '__main__':
    main()
