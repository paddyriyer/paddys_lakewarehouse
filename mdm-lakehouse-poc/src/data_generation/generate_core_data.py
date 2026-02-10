"""
Generate core Lakehouse data: Bronze → Silver → MDM → Gold star schema.

Produces:
  - bronze/sap_kna1.csv          (500 SAP customer records)
  - bronze/sfdc_accounts.csv     (400 Salesforce accounts)
  - gold/dim_customer.csv        (500 golden records after MDM)
  - gold/dim_product.csv         (80 products, 8 categories)
  - gold/dim_date.csv            (762 calendar days)
  - gold/fact_sales.csv          (3,500 order transactions)
  - gold/fact_interactions.csv   (6,000 customer touchpoints)
  - mdm/match_pairs.csv          (200 MDM candidate pairs)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid
import os

# Reproducible randomness
np.random.seed(42)
random.seed(42)

# ─── Configuration ───
N_CUSTOMERS = 500
N_PRODUCTS = 80
N_ORDERS = 3500
N_INTERACTIONS = 6000
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

# ─── Helpers ───
def uid():
    return str(uuid.uuid4())[:12]

def rand_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# ─── Reference data ───
COUNTRIES = ['US', 'US', 'US', 'US', 'UK', 'UK', 'DE', 'FR', 'IN', 'CA', 'AU', 'JP', 'BR', 'SG']
SEGMENTS = ['Enterprise', 'Mid-Market', 'SMB', 'Startup']
INDUSTRIES = ['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing', 'Media', 'Energy', 'Education']
SOURCES = ['SAP', 'Salesforce', 'Oracle', 'E-Commerce']
CHANNELS = ['Email', 'Phone', 'Web Chat', 'In-Person', 'Social Media']
STATUSES = ['Active', 'Churned', 'At-Risk', 'New']
CATEGORIES = ['Software License', 'Cloud Platform', 'Professional Services',
              'Support & Maintenance', 'Hardware', 'Training', 'Data Analytics', 'Security Suite']
CITIES = ['New York', 'San Francisco', 'London', 'Berlin', 'Paris',
          'Mumbai', 'Toronto', 'Sydney', 'Tokyo', 'Singapore']


def generate_bronze():
    """Phase 1: Generate raw source system extracts (Bronze layer)."""
    print("  Generating Bronze layer...")

    # SAP KNA1 (Customer Master)
    sap = []
    for i in range(N_CUSTOMERS):
        sap.append({
            'KUNNR': f'KNA{i+1:06d}',
            'NAME1': f'Customer_{i+1}' if i % 10 != 0 else f'Acme Corp Variant {i}',
            'LAND1': random.choice(COUNTRIES),
            'ORT01': random.choice(CITIES),
            'PSTLZ': f'{random.randint(10000, 99999)}',
            'TELF1': f'+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}',
            'SMTP_ADDR': f'contact_{i+1}@company{i+1}.com',
            '_source_system': 'SAP_ECC',
            '_ingestion_ts': datetime.now().isoformat(),
        })

    # Salesforce Accounts (overlapping ~60% with SAP)
    sfdc = []
    for i in range(int(N_CUSTOMERS * 0.8)):
        overlap = i < int(N_CUSTOMERS * 0.6)
        sfdc.append({
            'Id': f'001{uid()}',
            'Name': f'Customer_{i+1}' if overlap else f'NewCo_{i+1}',
            'BillingCountry': random.choice(COUNTRIES),
            'BillingCity': random.choice(CITIES),
            'Phone': f'+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}',
            'Website': f'https://company{i+1}.com',
            'Industry': random.choice(INDUSTRIES),
            'AnnualRevenue': round(random.uniform(100000, 50000000), 2),
            'NumberOfEmployees': random.randint(10, 50000),
            '_source_system': 'SALESFORCE',
            '_ingestion_ts': datetime.now().isoformat(),
        })

    pd.DataFrame(sap).to_csv(os.path.join(OUTPUT_DIR, 'bronze', 'sap_kna1.csv'), index=False)
    pd.DataFrame(sfdc).to_csv(os.path.join(OUTPUT_DIR, 'bronze', 'sfdc_accounts.csv'), index=False)
    print(f"    SAP KNA1: {len(sap)} records | SFDC Accounts: {len(sfdc)} records")


def generate_gold():
    """Phase 2: Generate Gold star schema (after Silver + MDM processing)."""
    print("  Generating Gold layer...")

    # dim_customer (Golden Records after MDM merge)
    customers = []
    for i in range(N_CUSTOMERS):
        status = random.choices(STATUSES, weights=[60, 10, 15, 15])[0]
        customers.append({
            'customer_uid': f'CUST-{uid()}',
            'full_name': f'Customer {i+1} Corp',
            'email': f'contact@customer{i+1}.com',
            'phone': f'+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}',
            'country': random.choice(COUNTRIES),
            'city': random.choice(CITIES),
            'segment': random.choice(SEGMENTS),
            'industry': random.choice(INDUSTRIES),
            'status': status,
            'source_systems': random.choice([
                'SAP+Salesforce', 'SAP+Oracle', 'Salesforce+Oracle',
                'SAP', 'Salesforce', 'SAP+Salesforce+Oracle'
            ]),
            'match_score': round(random.uniform(0.75, 1.0), 3) if random.random() > 0.3 else None,
            'lifetime_value': round(random.uniform(5000, 2000000), 2),
            'employee_count': random.randint(10, 50000),
            'annual_revenue': round(random.uniform(100000, 50000000), 2),
            'created_date': rand_date(datetime(2020, 1, 1), datetime(2024, 6, 1)).strftime('%Y-%m-%d'),
            'last_activity_date': rand_date(datetime(2025, 6, 1), datetime(2026, 1, 31)).strftime('%Y-%m-%d'),
            'is_current': True,
        })
    df_customers = pd.DataFrame(customers)

    # dim_product
    products = []
    for i in range(N_PRODUCTS):
        cat = random.choice(CATEGORIES)
        unit_price = round(random.uniform(99, 250000), 2)
        cost_price = round(random.uniform(50, min(unit_price * 0.7, unit_price - 1)), 2)
        products.append({
            'product_id': f'PROD-{i+1:04d}',
            'product_name': f'{cat} {"Premium" if random.random() > 0.5 else "Standard"} v{random.randint(1, 5)}',
            'category': cat,
            'subcategory': random.choice(['Basic', 'Pro', 'Enterprise', 'Ultimate']),
            'unit_price': unit_price,
            'cost_price': cost_price,
            'margin_pct': round((unit_price - cost_price) / unit_price * 100, 1),
            'is_recurring': cat in ['Software License', 'Cloud Platform', 'Support & Maintenance'],
            'launch_date': rand_date(datetime(2020, 1, 1), datetime(2025, 6, 1)).strftime('%Y-%m-%d'),
            'is_active': random.random() > 0.1,
        })
    df_products = pd.DataFrame(products)

    # dim_date
    dates = pd.date_range('2024-01-01', '2026-01-31', freq='D')
    df_dates = pd.DataFrame({
        'date_key': dates.strftime('%Y-%m-%d'),
        'year': dates.year,
        'quarter': dates.quarter,
        'month': dates.month,
        'month_name': dates.strftime('%b'),
        'week': dates.isocalendar().week.values,
        'day_of_week': dates.strftime('%A'),
        'is_weekend': dates.dayofweek >= 5,
    })

    # fact_sales
    orders = []
    for i in range(N_ORDERS):
        cust = random.choice(customers)
        prod = random.choice(products)
        order_date = rand_date(datetime(2024, 1, 1), datetime(2026, 1, 31))
        qty = random.randint(1, 50)
        discount = random.choice([0, 0, 0, 5, 10, 15, 20])
        line_total = round(qty * prod['unit_price'] * (1 - discount / 100), 2)
        orders.append({
            'order_id': f'ORD-{i+1:06d}',
            'customer_uid': cust['customer_uid'],
            'product_id': prod['product_id'],
            'order_date': order_date.strftime('%Y-%m-%d'),
            'quantity': qty,
            'unit_price': prod['unit_price'],
            'discount_pct': discount,
            'line_total': line_total,
            'cost_total': round(qty * prod['cost_price'], 2),
            'profit': round(line_total - qty * prod['cost_price'], 2),
            'order_source': random.choice(SOURCES),
            'region': cust['country'],
            'sales_rep': f'Rep_{random.randint(1, 25)}',
        })
    df_orders = pd.DataFrame(orders)

    # fact_interactions
    interactions = []
    for i in range(N_INTERACTIONS):
        cust = random.choice(customers)
        int_date = rand_date(datetime(2024, 1, 1), datetime(2026, 1, 31))
        interactions.append({
            'interaction_id': f'INT-{i+1:06d}',
            'customer_uid': cust['customer_uid'],
            'interaction_date': int_date.strftime('%Y-%m-%d'),
            'channel': random.choice(CHANNELS),
            'interaction_type': random.choice([
                'Inquiry', 'Support Ticket', 'Demo Request',
                'Renewal', 'Complaint', 'Feedback', 'Upsell Opportunity'
            ]),
            'sentiment': random.choices(['Positive', 'Neutral', 'Negative'], weights=[50, 35, 15])[0],
            'resolution_hours': round(random.uniform(0.5, 72), 1),
            'csat_score': random.choice([None, None, 1, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5]),
        })
    df_interactions = pd.DataFrame(interactions)

    # Save Gold layer
    df_customers.to_csv(os.path.join(OUTPUT_DIR, 'gold', 'dim_customer.csv'), index=False)
    df_products.to_csv(os.path.join(OUTPUT_DIR, 'gold', 'dim_product.csv'), index=False)
    df_dates.to_csv(os.path.join(OUTPUT_DIR, 'gold', 'dim_date.csv'), index=False)
    df_orders.to_csv(os.path.join(OUTPUT_DIR, 'gold', 'fact_sales.csv'), index=False)
    df_interactions.to_csv(os.path.join(OUTPUT_DIR, 'gold', 'fact_interactions.csv'), index=False)

    print(f"    dim_customer: {len(df_customers)} | dim_product: {len(df_products)}")
    print(f"    fact_sales: {len(df_orders)} | fact_interactions: {len(df_interactions)}")

    return customers, products


def generate_mdm(customers):
    """Phase 3: Generate MDM match pair results."""
    print("  Generating MDM match pairs...")
    match_pairs = []
    for i in range(200):
        match_pairs.append({
            'pair_id': f'MP-{i+1:04d}',
            'customer_a': random.choice(customers)['customer_uid'],
            'customer_b': random.choice(customers)['customer_uid'],
            'match_score': round(random.uniform(0.65, 1.0), 3),
            'match_tier': random.choices(
                ['AUTO_MERGE', 'REVIEW', 'NO_MATCH'], weights=[60, 25, 15]
            )[0],
            'name_similarity': round(random.uniform(0.5, 1.0), 3),
            'email_match': random.choice([True, False]),
            'phone_match': random.choice([True, False]),
            'address_similarity': round(random.uniform(0.3, 1.0), 3),
        })
    df = pd.DataFrame(match_pairs)
    df.to_csv(os.path.join(OUTPUT_DIR, 'mdm', 'match_pairs.csv'), index=False)
    print(f"    Match pairs: {len(df)} ({df['match_tier'].value_counts().to_dict()})")


def main():
    """Generate all core data."""
    print("=" * 60)
    print("CORE DATA GENERATION — Bronze → Silver → MDM → Gold")
    print("=" * 60)

    # Ensure directories exist
    for sub in ['bronze', 'silver', 'mdm', 'gold']:
        os.makedirs(os.path.join(OUTPUT_DIR, sub), exist_ok=True)

    generate_bronze()
    customers, products = generate_gold()
    generate_mdm(customers)

    print("\n✅ Core data generation complete!")
    print(f"   Output: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
