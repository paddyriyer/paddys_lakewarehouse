"""
Generate fraud tracking signals (fact_fraud_signals).

Simulates anomaly detection across 12 fraud types with severity scoring,
multiple detection methods (ML, Claude AI, Rule-Based), and resolution tracking.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'fraud')

FRAUD_TYPES = ['Duplicate Invoice', 'Velocity Anomaly', 'Amount Spike', 'Geo Mismatch',
               'After-Hours Access', 'Phantom Vendor', 'Identity Mismatch', 'Unusual Pattern',
               'Round Amount', 'Sequential IDs', 'Split Transaction', 'PO Mismatch']
SEVERITIES = ['Critical', 'High', 'Medium', 'Low']
STATUSES = ['Open', 'Investigating', 'Confirmed Fraud', 'False Positive', 'Resolved']
DETECTION_METHODS = ['ML Anomaly Model', 'Rule-Based', 'Claude AI Analysis', 'Manual Review', 'Pattern Matching']
TEAMS = ['Fraud Ops', 'Data Quality', 'Finance', 'Security', 'Compliance']


def generate_fraud(customer_uids: list, n_alerts: int = 450):
    """Generate fraud alert signals."""
    print(f"  Generating {n_alerts} fraud alerts...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    alerts = []
    for i in range(n_alerts):
        detected = datetime(2024, 6, 1) + timedelta(days=random.randint(0, 609))
        fraud_type = random.choice(FRAUD_TYPES)
        sev = random.choices(SEVERITIES, weights=[5, 15, 40, 40])[0]

        # Risk score based on severity
        risk_score = round(max(1, min(100, {
            'Critical': random.gauss(90, 5),
            'High': random.gauss(70, 10),
            'Medium': random.gauss(45, 12),
            'Low': random.gauss(20, 8),
        }[sev])), 1)

        # Status distribution varies by severity
        status_weights = ([10, 15, 8, 40, 27] if sev in ['Low', 'Medium']
                          else [15, 25, 20, 15, 25])
        status = random.choices(STATUSES, weights=status_weights)[0]

        amount = round(min(random.lognormvariate(10, 1.5), 2000000), 2)
        if fraud_type == 'Phantom Vendor':
            amount = round(random.uniform(50000, 500000), 2)

        alerts.append({
            'alert_id': f'FRD-{i+1:05d}',
            'detected_date': detected.strftime('%Y-%m-%d'),
            'detected_timestamp': detected.replace(
                hour=random.randint(0, 23), minute=random.randint(0, 59)
            ).isoformat(),
            'customer_uid': random.choice(customer_uids),
            'related_order_id': f'ORD-{random.randint(1, 3500):06d}' if random.random() > 0.2 else None,
            'fraud_type': fraud_type,
            'severity': sev,
            'risk_score': risk_score,
            'flagged_amount': amount,
            'status': status,
            'is_confirmed_fraud': status == 'Confirmed Fraud',
            'is_false_positive': status == 'False Positive',
            'detection_method': random.choice(DETECTION_METHODS),
            'investigating_team': random.choice(TEAMS),
            'resolution_hours': (round(random.uniform(1, 240), 1)
                                 if status in ['Confirmed Fraud', 'False Positive', 'Resolved'] else None),
            'financial_impact': (round(amount * random.uniform(0, 0.3), 2)
                                 if status == 'Confirmed Fraud' else 0),
            'source_system': random.choice(['SAP', 'Salesforce', 'Oracle', 'E-Commerce', 'Payment Gateway']),
        })

    df = pd.DataFrame(alerts)
    df.to_csv(os.path.join(OUTPUT_DIR, 'fact_fraud_signals.csv'), index=False)

    confirmed = df[df['is_confirmed_fraud']]
    print(f"    Alerts: {len(df)} | Confirmed: {len(confirmed)} (${confirmed['financial_impact'].sum():,.0f})")
    print(f"    Severity: {df['severity'].value_counts().to_dict()}")
    return df
