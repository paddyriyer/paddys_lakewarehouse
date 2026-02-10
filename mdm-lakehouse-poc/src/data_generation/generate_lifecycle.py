"""
Generate customer lifecycle / livability data (dim_customer_lifecycle).

Models customer journey stages, cohort membership, churn risk scoring,
repeat purchase behavior, and health scores.

Lifecycle Stages:
  Champion  → 24+ months tenure, low churn risk
  Loyal     → 12-24 months, consistent engagement
  Growing   → 3-12 months, building relationship
  Activated → New customers (< 3 months)
  At-Risk   → 45-90 day activity gap
  Dormant   → 90+ day activity gap
  Churned   → Cancelled / lost customers
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'gold')


def generate_lifecycle(customers_df: pd.DataFrame):
    """Generate lifecycle dimension from customer data."""
    print("  Generating customer lifecycle data...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    records = []
    ref_date = datetime(2026, 2, 1)

    for _, c in customers_df.iterrows():
        created = datetime.strptime(c['created_date'], '%Y-%m-%d')
        last_activity = datetime.strptime(c['last_activity_date'], '%Y-%m-%d')
        tenure_days = (ref_date - created).days
        tenure_months = tenure_days // 30
        days_since_activity = (ref_date - last_activity).days

        # ── Lifecycle stage assignment logic ──
        if c['status'] == 'Churned':
            stage = 'Churned'
            churn_risk = 1.0
        elif c['status'] == 'New':
            stage = 'Onboarding' if tenure_months < 3 else 'Activated'
            churn_risk = round(random.uniform(0.05, 0.25), 3)
        elif days_since_activity > 90:
            stage = 'Dormant'
            churn_risk = round(random.uniform(0.60, 0.95), 3)
        elif days_since_activity > 45:
            stage = 'At-Risk'
            churn_risk = round(random.uniform(0.30, 0.65), 3)
        elif tenure_months > 24:
            stage = 'Champion'
            churn_risk = round(random.uniform(0.01, 0.10), 3)
        elif tenure_months > 12:
            stage = 'Loyal'
            churn_risk = round(random.uniform(0.05, 0.20), 3)
        else:
            stage = 'Growing'
            churn_risk = round(random.uniform(0.10, 0.35), 3)

        # ── Order behavior ──
        total_orders = random.randint(1, 30) if c['status'] != 'Churned' else random.randint(1, 5)
        repeat_orders = max(0, total_orders - 1)

        first_order = created + timedelta(days=random.randint(1, min(90, tenure_days)))
        last_order = last_activity - timedelta(days=random.randint(0, 60))
        if last_order < first_order:
            last_order = first_order

        health_score = round(100 - (churn_risk * 100) + random.uniform(-5, 5), 1)
        health_score = max(0, min(100, health_score))

        records.append({
            'customer_uid': c['customer_uid'],
            'cohort_month': created.strftime('%Y-%m'),
            'cohort_quarter': f"Q{(created.month - 1) // 3 + 1} {created.year}",
            'tenure_days': tenure_days,
            'tenure_months': tenure_months,
            'lifecycle_stage': stage,
            'churn_risk_score': churn_risk,
            'churn_risk_tier': 'High' if churn_risk >= 0.5 else 'Medium' if churn_risk >= 0.2 else 'Low',
            'total_orders': total_orders,
            'repeat_orders': repeat_orders,
            'is_repeat_customer': repeat_orders > 0,
            'first_order_date': first_order.strftime('%Y-%m-%d'),
            'last_order_date': last_order.strftime('%Y-%m-%d'),
            'days_since_last_order': (ref_date - last_order).days,
            'avg_order_frequency_days': round(tenure_days / max(total_orders, 1), 1),
            'predicted_ltv_12mo': round(c['lifetime_value'] * random.uniform(0.8, 1.4), 2),
            'nps_score': random.choice([None] + list(range(0, 11))),
            'health_score': health_score,
        })

    df = pd.DataFrame(records)
    df.to_csv(os.path.join(OUTPUT_DIR, 'dim_customer_lifecycle.csv'), index=False)

    print(f"    Stages: {df['lifecycle_stage'].value_counts().to_dict()}")
    print(f"    Churn tiers: {df['churn_risk_tier'].value_counts().to_dict()}")
    print(f"    Repeat rate: {df['is_repeat_customer'].mean()*100:.1f}%")
    return df
