# Dashboard Guide

## MDM Lakehouse Executive Dashboard — 8 Tabs

### Viewing the Dashboard

The dashboard is a single React JSX file (`src/dashboards/MDM_Dashboard.jsx`) that can be:

1. **Opened in Claude.ai** — Paste the JSX into Claude Artifacts for instant rendering
2. **Run locally** — Import into any React 18+ project with Recharts installed
3. **Deployed** — Build with Vite/Next.js for production hosting

### Dependencies

```bash
npm install react recharts
```

---

### Tab 1: ⚡ Executive Real-Time

**Purpose:** Live business pulse — the first thing executives see each morning.

| Widget | Data Source | What It Shows |
|--------|-----------|---------------|
| Active Users | fact_realtime_metrics | Current concurrent users with peak indicator |
| Revenue Today | fact_realtime_metrics | Same-day revenue with trend arrow |
| Pipeline Value | fact_pipeline | Total open deal value |
| New Leads | fact_realtime_metrics | Lead count with source breakdown |
| API Latency | fact_realtime_metrics | P50 response time |
| Fraud Alerts | fact_fraud_signals | Open alert count with critical highlight |
| Traffic Chart | fact_realtime_metrics | Hourly active users + latency overlay |
| Pipeline Funnel | fact_pipeline | Deals by stage (horizontal bar) |
| Fraud Severity | fact_fraud_signals | Donut chart by severity tier |
| Lifecycle Stages | dim_customer_lifecycle | Bar chart of customer stage distribution |

### Tab 2: 📊 Revenue Analytics

**Purpose:** Financial performance across time, categories, segments, and geographies.

- Monthly revenue vs profit bar chart (25 months)
- Revenue by product category (horizontal bars)
- Revenue by country (vertical bars, top 10)

### Tab 3: 👥 Customer 360

**Purpose:** Unified view of customer health, engagement, and sentiment.

- Customer status donut (Active/New/At-Risk/Churned)
- Sentiment analysis donut (Positive/Neutral/Negative from fact_interactions)
- Segment radar chart (Revenue + Customer count overlaid)

### Tab 4: 🔄 Customer Lifecycle

**Purpose:** Customer livability analysis — how long customers last, who's at risk.

- Lifecycle stage bar chart with color-coded stages
- Churn risk tier donut (High/Medium/Low)
- Action cards for each lifecycle stage with:
  - Stage name and color indicator
  - Tenure threshold
  - Description of customer behavior
  - Recommended action (e.g., "VIP programs, referral incentives")

### Tab 5: 🎯 GTM Pipeline

**Purpose:** Sales performance — funnel health, rep effectiveness, loss analysis.

- Pipeline funnel (deals by stage + value line overlay)
- Loss reasons horizontal bar chart
- Sales rep leaderboard table with win rate progress bars
- Lead source performance (won vs total stacked bars)

### Tab 6: 🖱️ Clickstream

**Purpose:** Web analytics — traffic sources, conversion funnels, campaign attribution.

- Conversion funnel bar chart (Homepage → Products → Pricing → Demo → Checkout)
- Referrer source chart with visits bars + conversion rate line
- UTM campaign cards showing conversion rate and lead volume per campaign

### Tab 7: 🛡️ Fraud Tracking

**Purpose:** Anomaly monitoring — alerts, severity, detection effectiveness.

- Severity distribution donut
- Alert status donut (Open/Investigating/Confirmed/False Positive/Resolved)
- Detection methods horizontal bar (ML Anomaly, Claude AI, Rule-Based, etc.)
- Fraud types bar chart (12 types)
- Active critical alerts panel with risk scores and source systems

### Tab 8: 🔗 MDM & Data Quality

**Purpose:** Data governance — match quality, source linkage, schema overview.

- MDM match tier donut (AUTO_MERGE/REVIEW/NO_MATCH)
- Source system linkage bar (shows cross-system customer linking)
- Full 11-table schema ERD showing table name, type, row count, and key columns

---

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| AWS Orange | `#FF9900` | Primary accent, revenue metrics |
| Purple | `#8B5CF6` | Data/MDM metrics |
| Cyan | `#06B6D4` | Real-time/tech metrics |
| Green | `#10B981` | Positive outcomes, success |
| Red | `#EF4444` | Alerts, churn, fraud |
| Gold | `#F59E0B` | Warnings, at-risk |
| Blue | `#3B82F6` | General analytics |
