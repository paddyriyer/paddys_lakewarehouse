"""
Generate clickstream / web analytics data (fact_clickstream).

Simulates 25,000 web events including page views, form submissions,
button clicks, video plays, and conversions across multiple referrer
sources and UTM campaigns.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'clickstream')

PAGES = ['/home', '/products', '/pricing', '/demo-request', '/docs', '/blog',
         '/case-studies', '/contact', '/login', '/dashboard', '/checkout',
         '/support', '/api-docs', '/about', '/careers', '/whitepaper',
         '/webinar-signup', '/free-trial']
DEVICES = ['Desktop', 'Mobile', 'Tablet']
BROWSERS = ['Chrome', 'Safari', 'Firefox', 'Edge']
REFERRERS = ['Google Search', 'Direct', 'LinkedIn', 'Twitter/X', 'Email Campaign',
             'Partner Referral', 'Paid Google', 'Paid LinkedIn', 'Organic Social', 'Bing']
EVENTS = ['page_view', 'button_click', 'form_submit', 'video_play', 'download',
          'search', 'add_to_cart', 'scroll_depth_75', 'chat_opened', 'pricing_toggle']
CAMPAIGNS = [None, None, 'spring_launch', 'q4_push', 'partner_webinar',
             'product_update', 'brand_awareness', 'retarget_q1']

# Business hours traffic weighting (index = hour)
HOURLY_WEIGHTS = [1,0,0,0,0,1,2,4,8,10,10,9,8,9,10,10,9,8,6,5,4,3,2,1]


def generate_clickstream(customer_uids: list, n_events: int = 25000):
    """Generate web clickstream events."""
    print(f"  Generating {n_events:,} clickstream events...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    events = []
    for i in range(n_events):
        ts = datetime(2024, 7, 1) + timedelta(days=random.randint(0, 579))
        hour = random.choices(range(24), weights=HOURLY_WEIGHTS)[0]
        ts = ts.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))

        # 30% anonymous visitors, 70% known customers
        cuid = random.choice(customer_uids) if random.random() > 0.3 else None
        page = random.choice(PAGES)

        # Conversion-weighted events for key pages
        if page in ['/checkout', '/demo-request', '/free-trial']:
            event = random.choice(['page_view', 'form_submit', 'button_click'])
        else:
            event = random.choice(EVENTS)

        is_converted = 1 if (event == 'form_submit' and
                             page in ['/demo-request', '/free-trial', '/checkout']) else 0

        events.append({
            'event_id': f'EVT-{i+1:06d}',
            'session_id': f'SES-{random.randint(1, 8000):06d}',
            'customer_uid': cuid,
            'visitor_id': f'VIS-{random.randint(1, 2000):06d}' if not cuid else None,
            'event_timestamp': ts.isoformat(),
            'event_date': ts.strftime('%Y-%m-%d'),
            'page_url': page,
            'event_type': event,
            'device_type': random.choice(DEVICES),
            'browser': random.choice(BROWSERS),
            'referrer_source': random.choice(REFERRERS),
            'session_duration_sec': random.randint(5, 1800),
            'page_load_ms': random.randint(200, 5000),
            'is_converted': is_converted,
            'utm_campaign': random.choice(CAMPAIGNS),
            'country': random.choice(['US', 'US', 'US', 'UK', 'UK', 'DE', 'FR', 'IN', 'CA', 'AU']),
        })

    df = pd.DataFrame(events)
    df.to_csv(os.path.join(OUTPUT_DIR, 'fact_clickstream.csv'), index=False)

    conversions = df['is_converted'].sum()
    print(f"    Events: {len(df):,} | Conversions: {conversions} ({conversions/len(df)*100:.1f}%)")
    return df
