"""
Generate GTM sales pipeline data (fact_pipeline).
Models full sales funnel: Lead → MQL → SQL → Discovery → Proposal → Negotiation → Won/Lost
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'pipeline')
STAGES = ['Lead', 'MQL', 'SQL', 'Discovery', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
STAGE_PROBS = [1.0, 0.65, 0.45, 0.35, 0.25, 0.18, 0.12, 0.08]
LEAD_SOURCES = ['Inbound Web', 'Outbound SDR', 'Partner Referral', 'Event/Conference',
                'Content Download', 'Paid Campaign', 'Existing Customer', 'Product-Led']
COMPETITORS = [None, None, None, 'Informatica', 'Reltio', 'Tamr', 'Semarchy', 'Profisee']
LOSS_REASONS = ['Price', 'Timing', 'Competition', 'No Decision', 'Feature Gap']


def generate_pipeline(customer_uids: list, n_deals: int = 1200):
    """Generate GTM sales pipeline deals."""
    print(f"  Generating {n_deals} pipeline deals...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    deals = []
    for i in range(n_deals):
        created = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 745))
        deal_size = round(min(random.lognormvariate(12.5, 1.2), 5000000), 2)

        # Determine final stage
        final_idx = 0
        for idx in range(len(STAGES)):
            if random.random() < STAGE_PROBS[idx]:
                final_idx = idx
        final_stage = STAGES[final_idx]

        days_in_pipe = random.randint(5, 180)
        close_date = (created + timedelta(days=days_in_pipe)
                      if final_stage in ['Closed Won', 'Closed Lost'] else None)

        deals.append({
            'deal_id': f'DEAL-{i+1:05d}',
            'customer_uid': random.choice(customer_uids),
            'deal_name': f'{random.choice(["Enterprise", "Platform", "Suite"])} Deal #{i+1}',
            'deal_amount': deal_size,
            'current_stage': final_stage,
            'created_date': created.strftime('%Y-%m-%d'),
            'expected_close_date': (created + timedelta(days=days_in_pipe)).strftime('%Y-%m-%d'),
            'actual_close_date': close_date.strftime('%Y-%m-%d') if close_date else None,
            'lead_source': random.choice(LEAD_SOURCES),
            'sales_rep': f'Rep_{random.randint(1, 25)}',
            'is_won': final_stage == 'Closed Won',
            'is_lost': final_stage == 'Closed Lost',
            'is_open': final_stage not in ['Closed Won', 'Closed Lost'],
            'days_in_pipeline': days_in_pipe,
            'product_interest': random.choice(['Cloud Platform', 'Security Suite', 'Data Analytics', 'Full Suite']),
            'competitor': random.choice(COMPETITORS),
            'loss_reason': random.choice(LOSS_REASONS) if final_stage == 'Closed Lost' else None,
        })

    df = pd.DataFrame(deals)
    df.to_csv(os.path.join(OUTPUT_DIR, 'fact_pipeline.csv'), index=False)

    won = df[df['is_won']]
    print(f"    Deals: {len(df)} | Won: {len(won)} (${won['deal_amount'].sum()/1e6:.1f}M)")
    print(f"    Win rate: {len(won) / (len(won) + len(df[df['is_lost']])) * 100:.1f}%")
    return df
