"""
Data Quality Validation Tests
===============================
Validates the generated sample data meets quality expectations.
Run: pytest tests/test_data_quality.py -v
"""

import pytest
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


class TestDimCustomer:
    @pytest.fixture(autouse=True)
    def load(self):
        self.df = pd.read_csv(os.path.join(DATA_DIR, 'gold', 'dim_customer.csv'))

    def test_row_count(self):
        assert len(self.df) == 500, f"Expected 500 customers, got {len(self.df)}"

    def test_no_null_primary_key(self):
        assert self.df['customer_uid'].notna().all(), "customer_uid has nulls"

    def test_unique_primary_key(self):
        assert self.df['customer_uid'].is_unique, "customer_uid is not unique"

    def test_valid_segments(self):
        valid = {'Enterprise', 'Mid-Market', 'SMB', 'Startup'}
        assert set(self.df['segment'].unique()) <= valid

    def test_valid_statuses(self):
        valid = {'Active', 'Churned', 'At-Risk', 'New'}
        assert set(self.df['status'].unique()) <= valid

    def test_lifetime_value_positive(self):
        assert (self.df['lifetime_value'] > 0).all()


class TestDimProduct:
    @pytest.fixture(autouse=True)
    def load(self):
        self.df = pd.read_csv(os.path.join(DATA_DIR, 'gold', 'dim_product.csv'))

    def test_row_count(self):
        assert len(self.df) == 80

    def test_margin_calculation(self):
        expected = ((self.df['unit_price'] - self.df['cost_price']) / self.df['unit_price'] * 100).round(1)
        pd.testing.assert_series_equal(self.df['margin_pct'], expected, check_names=False)

    def test_cost_less_than_price(self):
        assert (self.df['cost_price'] <= self.df['unit_price']).all()


class TestFactSales:
    @pytest.fixture(autouse=True)
    def load(self):
        self.df = pd.read_csv(os.path.join(DATA_DIR, 'gold', 'fact_sales.csv'))
        self.customers = pd.read_csv(os.path.join(DATA_DIR, 'gold', 'dim_customer.csv'))

    def test_row_count(self):
        assert len(self.df) == 3500

    def test_referential_integrity_customer(self):
        valid_uids = set(self.customers['customer_uid'])
        assert self.df['customer_uid'].isin(valid_uids).all(), "Orphan customer UIDs in fact_sales"

    def test_no_negative_revenue(self):
        assert (self.df['line_total'] >= 0).all()


class TestFactClickstream:
    @pytest.fixture(autouse=True)
    def load(self):
        self.df = pd.read_csv(os.path.join(DATA_DIR, 'clickstream', 'fact_clickstream.csv'))

    def test_row_count(self):
        assert len(self.df) == 25000

    def test_conversion_flag_binary(self):
        assert set(self.df['is_converted'].unique()) <= {0, 1}

    def test_anonymous_rate(self):
        anon_rate = self.df['customer_uid'].isna().mean()
        assert 0.2 < anon_rate < 0.4, f"Anonymous rate {anon_rate:.2%} outside expected 20-40%"


class TestFactFraud:
    @pytest.fixture(autouse=True)
    def load(self):
        self.df = pd.read_csv(os.path.join(DATA_DIR, 'fraud', 'fact_fraud_signals.csv'))

    def test_row_count(self):
        assert len(self.df) == 450

    def test_risk_score_bounds(self):
        assert (self.df['risk_score'] >= 1).all()
        assert (self.df['risk_score'] <= 100).all()

    def test_severity_values(self):
        valid = {'Critical', 'High', 'Medium', 'Low'}
        assert set(self.df['severity'].unique()) <= valid

    def test_confirmed_has_impact(self):
        confirmed = self.df[self.df['is_confirmed_fraud']]
        assert (confirmed['financial_impact'] >= 0).all()


class TestMDMMatchPairs:
    @pytest.fixture(autouse=True)
    def load(self):
        self.df = pd.read_csv(os.path.join(DATA_DIR, 'mdm', 'mdm_match_pairs.csv'))

    def test_row_count(self):
        assert len(self.df) == 200

    def test_match_score_range(self):
        assert (self.df['match_score'] >= 0).all()
        assert (self.df['match_score'] <= 1).all()

    def test_tier_classification(self):
        valid = {'AUTO_MERGE', 'REVIEW', 'NO_MATCH'}
        assert set(self.df['match_tier'].unique()) <= valid
