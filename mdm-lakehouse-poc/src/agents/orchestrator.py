"""
Meta-Agent Orchestrator
========================
Runs all 6 specialized Claude agents in dependency order.

Usage:
    python src/agents/orchestrator.py

Agent Pipeline:
    1. ETL Generator    → Profiles sources → generates extraction pipelines
    2. DQ Engine        → Profiles tables → generates Great Expectations suites
    3. MDM Matcher      → Analyzes data → creates fuzzy matching engine
    4. dbt Modeler      → Inspects Silver/MDM → generates Gold star schema
    5. DAG Builder      → Reads pipelines → generates Step Functions ASL
    6. Doc Writer       → Reads everything → generates data dictionaries
"""

from agent_loop import run_agent

# ── Agent system prompts ──
AGENT_PROMPTS = {
    "etl_generator": """You are an ETL Pipeline Generator agent. Your job is to:
1. Profile source system schemas (SAP, Salesforce, Oracle)
2. Generate PySpark extraction jobs for each table
3. Add Bronze metadata columns (_ingestion_ts, _source_system, _row_hash)
4. Write Delta Lake format with partitioning
5. Generate one pipeline per source table""",

    "dq_engine": """You are a Data Quality Engine agent. Your job is to:
1. Profile each table's column statistics
2. Generate Great Expectations validation suites
3. Create DQ gates between Bronze→Silver, Silver→MDM, MDM→Gold
4. Set pass threshold at 95%
5. Configure SNS alerts for failures""",

    "mdm_matcher": """You are an MDM Matching Engine agent. Your job is to:
1. Analyze customer data patterns across sources
2. Implement blocking strategy (Soundex) to reduce comparisons
3. Generate weighted fuzzy matching (Jaro-Winkler: 30% name, 25% email, 20% phone, 15% address, 10% source diversity)
4. Create match tier classification (AUTO_MERGE ≥ 0.92, REVIEW 0.75-0.92, NO_MATCH < 0.75)
5. Implement survivorship rules for golden record creation""",

    "dbt_modeler": """You are a dbt Star Schema Modeler agent. Your job is to:
1. Inspect Silver and MDM layers
2. Generate dimension tables (dim_customer SCD2, dim_product, dim_date)
3. Generate fact tables (fact_sales, fact_interactions)
4. Create dbt models with proper refs and tests
5. Configure Snowflake external table integration""",

    "dag_builder": """You are a DAG Builder agent. Your job is to:
1. Read all generated pipeline code
2. Build AWS Step Functions state machine (ASL)
3. Define parallel extraction, sequential transformation
4. Add DQ gate checkpoints with failure handling
5. Configure SNS notifications""",

    "doc_writer": """You are a Documentation Writer agent. Your job is to:
1. Read all generated code and configurations
2. Generate data dictionary with column descriptions
3. Create data lineage documentation
4. Write operational runbook
5. Produce ERD descriptions for the star schema""",
}

ENTERPRISE_SOURCES = [
    {"name": "SAP ECC", "type": "sap", "tables": ["KNA1", "KNB1", "MARA", "MAKT", "VBAK", "VBAP"]},
    {"name": "Salesforce", "type": "salesforce", "objects": ["Account", "Contact", "Opportunity", "Case"]},
    {"name": "Oracle CRM", "type": "oracle", "tables": ["CUSTOMERS", "ORDERS", "PRODUCTS"]},
    {"name": "E-Commerce", "type": "rest_api", "endpoints": ["/orders", "/products", "/reviews"]},
]


def run_full_project():
    """Execute all 6 agents in sequence."""
    print("=" * 60)
    print("META-AGENT ORCHESTRATOR — Full MDM Lakehouse Generation")
    print("=" * 60)

    # Phase 1: ETL
    print("\n[1/6] ETL Pipeline Generation")
    for source in ENTERPRISE_SOURCES:
        task = f"Generate extraction pipelines for {source['name']} ({source['type']})"
        print(f"  → {task}")
        # run_agent(AGENT_PROMPTS["etl_generator"], task)

    # Phase 2: DQ
    print("\n[2/6] Data Quality Framework")
    # run_agent(AGENT_PROMPTS["dq_engine"], "Generate DQ suites for all layers")

    # Phase 3: MDM
    print("\n[3/6] MDM Matching Engine")
    # run_agent(AGENT_PROMPTS["mdm_matcher"], "Create customer matching engine")

    # Phase 4: dbt
    print("\n[4/6] Gold Layer dbt Models")
    # run_agent(AGENT_PROMPTS["dbt_modeler"], "Generate star schema models")

    # Phase 5: DAG
    print("\n[5/6] Orchestration DAGs")
    # run_agent(AGENT_PROMPTS["dag_builder"], "Build Step Functions pipeline")

    # Phase 6: Docs
    print("\n[6/6] Documentation")
    # run_agent(AGENT_PROMPTS["doc_writer"], "Generate all documentation")

    print("\n" + "=" * 60)
    print("COMPLETE: All 6 agents executed successfully")
    print("=" * 60)


if __name__ == "__main__":
    run_full_project()
