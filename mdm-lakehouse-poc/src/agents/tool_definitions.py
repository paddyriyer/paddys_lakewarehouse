"""
Enterprise Data Tool Definitions
=================================
JSON Schema definitions for tools that Claude agents can invoke.
Each tool maps to a real handler function (see tool_handlers.py).
"""

ENTERPRISE_DATA_TOOLS = [
    {
        "name": "query_database",
        "description": "Execute SQL query against SAP HANA, Oracle, SQL Server, or Snowflake.",
        "input_schema": {
            "type": "object",
            "properties": {
                "connection": {
                    "type": "string",
                    "enum": ["sap_hana", "oracle", "sqlserver", "snowflake"],
                    "description": "Target database connection"
                },
                "sql": {"type": "string", "description": "SQL query to execute"},
                "max_rows": {"type": "integer", "default": 1000}
            },
            "required": ["connection", "sql"]
        }
    },
    {
        "name": "profile_data_source",
        "description": "Discover schema, column stats, null rates, cardinality for a table.",
        "input_schema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source system name"},
                "table": {"type": "string", "description": "Table name to profile"}
            },
            "required": ["source", "table"]
        }
    },
    {
        "name": "write_pipeline_code",
        "description": "Write a PySpark, dbt, Airflow, or Python file to the git repo.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "content": {"type": "string", "description": "File content to write"},
                "language": {
                    "type": "string",
                    "enum": ["pyspark", "dbt_sql", "airflow", "python"]
                }
            },
            "required": ["filename", "content"]
        }
    },
    {
        "name": "run_tests",
        "description": "Execute pytest, dbt test, or Great Expectations validation suite.",
        "input_schema": {
            "type": "object",
            "properties": {
                "test_type": {
                    "type": "string",
                    "enum": ["pytest", "dbt_test", "great_expectations"]
                },
                "target": {"type": "string", "description": "Test target path or table"}
            },
            "required": ["test_type", "target"]
        }
    },
    {
        "name": "salesforce_query",
        "description": "Execute SOQL query against Salesforce via simple_salesforce.",
        "input_schema": {
            "type": "object",
            "properties": {
                "soql": {"type": "string", "description": "SOQL query"},
                "object_name": {"type": "string"}
            },
            "required": ["soql"]
        }
    },
    {
        "name": "create_glue_job",
        "description": "Create and optionally start an AWS Glue ETL job.",
        "input_schema": {
            "type": "object",
            "properties": {
                "job_name": {"type": "string"},
                "script_location": {"type": "string"},
                "role": {"type": "string"},
                "start_immediately": {"type": "boolean", "default": False}
            },
            "required": ["job_name", "script_location"]
        }
    },
    {
        "name": "delta_lake_operation",
        "description": "Perform Delta Lake operations: read, write, merge, vacuum, history.",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["read", "write", "merge", "vacuum", "history", "describe"]
                },
                "path": {"type": "string", "description": "S3 path to Delta table"},
                "query": {"type": "string", "description": "Optional SQL for read/merge"}
            },
            "required": ["operation", "path"]
        }
    },
]
