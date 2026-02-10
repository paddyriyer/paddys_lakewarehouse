# Data Model Reference

## Star Schema — 11 Tables, 36,650+ Records

### Dimensions

#### dim_customer (500 rows)
Golden customer records produced by MDM matching engine.

| Column | Type | Description |
|--------|------|-------------|
| customer_uid | PK | Golden record unique ID (e.g., `CUST-f368991a`) |
| full_name | string | Merged customer name |
| email | string | Primary email (survivorship: most recent) |
| phone | string | Primary phone |
| country | string | ISO 2-letter country code |
| city | string | City name |
| segment | string | Enterprise, Mid-Market, SMB, Startup |
| industry | string | 8 industry categories |
| status | string | Active, At-Risk, Churned, New |
| source_systems | string | Contributing systems (e.g., "SAP+Salesforce") |
| match_score | float | MDM confidence score (0.75-1.0) |
| lifetime_value | float | Historical LTV in USD |
| created_date | date | First appearance in any source system |
| last_activity_date | date | Most recent interaction/order |
| is_current | bool | SCD2 current record flag |

#### dim_product (80 rows)

| Column | Type | Description |
|--------|------|-------------|
| product_id | PK | Product identifier (e.g., `PROD-0042`) |
| product_name | string | Full product name with tier |
| category | string | 8 categories (Software License, Cloud Platform, etc.) |
| subcategory | string | Basic, Pro, Enterprise, Ultimate |
| unit_price | float | List price in USD |
| cost_price | float | Cost basis |
| margin_pct | float | Gross margin percentage |
| is_recurring | bool | Subscription/recurring revenue flag |
| is_active | bool | Currently sold (90% active) |

#### dim_customer_lifecycle (500 rows)

| Column | Type | Description |
|--------|------|-------------|
| customer_uid | FK → dim_customer | Customer reference |
| cohort_month | string | First purchase month (e.g., "2022-03") |
| cohort_quarter | string | Cohort quarter (e.g., "Q1 2022") |
| tenure_months | int | Months since first appearance |
| lifecycle_stage | string | Champion, Loyal, Growing, Activated, At-Risk, Dormant, Churned |
| churn_risk_score | float | 0.0 (no risk) to 1.0 (certain churn) |
| churn_risk_tier | string | Low (<0.2), Medium (0.2-0.5), High (≥0.5) |
| total_orders | int | Lifetime order count |
| is_repeat_customer | bool | Has placed 2+ orders |
| health_score | float | 0-100 composite health metric |
| nps_score | int | Net Promoter Score (0-10, nullable) |

#### dim_date (762 rows)

| Column | Type | Description |
|--------|------|-------------|
| date_key | PK | ISO date string (e.g., "2024-07-15") |
| year | int | Calendar year |
| quarter | int | Quarter (1-4) |
| month | int | Month (1-12) |
| month_name | string | Abbreviated month (Jan, Feb...) |
| week | int | ISO week number |
| day_of_week | string | Full day name |
| is_weekend | bool | Saturday/Sunday flag |

### Facts

#### fact_sales (3,500 rows)

| Column | Type | Description |
|--------|------|-------------|
| order_id | PK | Order identifier |
| customer_uid | FK → dim_customer | Customer reference |
| product_id | FK → dim_product | Product reference |
| order_date | FK → dim_date | Order date |
| quantity | int | Units ordered |
| unit_price | float | Price per unit at time of sale |
| discount_pct | int | Discount applied (0, 5, 10, 15, 20) |
| line_total | float | Revenue: qty × price × (1 - discount) |
| cost_total | float | Cost: qty × cost_price |
| profit | float | line_total - cost_total |
| order_source | string | SAP, Salesforce, Oracle, E-Commerce |
| sales_rep | string | Assigned sales representative |

#### fact_clickstream (25,000 rows)

| Column | Type | Description |
|--------|------|-------------|
| event_id | PK | Unique event ID |
| session_id | string | Browser session grouping |
| customer_uid | FK (nullable) | Known customer (70%) or NULL (anonymous 30%) |
| visitor_id | string | Anonymous visitor tracking ID |
| event_timestamp | datetime | Event time (ISO format) |
| page_url | string | 18 possible page paths |
| event_type | string | page_view, form_submit, button_click, etc. |
| device_type | string | Desktop, Mobile, Tablet |
| referrer_source | string | Google Search, LinkedIn, Email Campaign, etc. |
| is_converted | int | 1 if conversion event, 0 otherwise |
| utm_campaign | string | Campaign tag (nullable) |

#### fact_pipeline (1,200 rows)

| Column | Type | Description |
|--------|------|-------------|
| deal_id | PK | Deal identifier |
| customer_uid | FK → dim_customer | Associated customer |
| deal_amount | float | Deal value in USD (log-normal distribution) |
| current_stage | string | Lead, MQL, SQL, Discovery, Proposal, Negotiation, Won, Lost |
| lead_source | string | Inbound Web, Outbound SDR, Partner Referral, etc. |
| sales_rep | string | Assigned rep (25 reps) |
| is_won / is_lost / is_open | bool | Outcome flags |
| loss_reason | string | Price, Feature Gap, No Decision, Timing, Competition |

#### fact_fraud_signals (450 rows)

| Column | Type | Description |
|--------|------|-------------|
| alert_id | PK | Alert identifier |
| fraud_type | string | 12 types (Split Transaction, Phantom Vendor, etc.) |
| severity | string | Critical, High, Medium, Low |
| risk_score | float | 1-100 composite risk score |
| status | string | Open, Investigating, Confirmed Fraud, False Positive, Resolved |
| detection_method | string | ML Anomaly Model, Claude AI Analysis, Rule-Based, etc. |
| financial_impact | float | Confirmed loss amount (0 if not confirmed) |

#### fact_realtime_metrics (168 rows)

| Column | Type | Description |
|--------|------|-------------|
| timestamp | PK | Hourly timestamp |
| active_users | int | Concurrent users |
| page_views | int | Hourly page views |
| api_calls | int | API request volume |
| avg_response_ms | float | P50 latency |
| error_rate_pct | float | Error percentage |
| dq_pass_rate | float | Data quality gate pass rate |

### Audit

#### mdm_match_pairs (200 rows)

| Column | Type | Description |
|--------|------|-------------|
| pair_id | PK | Match pair identifier |
| customer_a / customer_b | FK | Two candidate customers |
| match_score | float | Composite similarity (0.65-1.0) |
| match_tier | string | AUTO_MERGE (≥0.92), REVIEW (0.75-0.92), NO_MATCH (<0.75) |
| name_similarity | float | Jaro-Winkler on name field |
| email_match | bool | Exact email match |
| phone_match | bool | Phone number match |
| address_similarity | float | Jaro-Winkler on address |
