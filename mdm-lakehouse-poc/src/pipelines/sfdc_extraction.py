"""
Salesforce Account Extraction Pipeline
========================================
Two patterns: Batch (Bulk API 2.0) and Real-time (CDC via EventBridge).
"""

import boto3
import json
from datetime import datetime
from simple_salesforce import Salesforce


def get_sfdc_credentials():
    """Retrieve Salesforce credentials from Secrets Manager."""
    secrets = boto3.client('secretsmanager')
    resp = secrets.get_secret_value(SecretId='mdm/salesforce/production')
    return json.loads(resp['SecretString'])


# ═══════════════════════════════════════
# PATTERN 1: Batch Extraction (Bulk API)
# ═══════════════════════════════════════

def extract_accounts_batch(last_modified_after: str = None):
    """
    Incremental batch extraction via Salesforce Bulk API 2.0.
    Runs daily via AWS Glue schedule.
    """
    creds = get_sfdc_credentials()
    sf = Salesforce(
        username=creds['username'],
        password=creds['password'],
        security_token=creds['security_token'],
        domain='login',
    )

    soql = """
        SELECT Id, Name, BillingCountry, BillingCity, BillingStreet,
               Phone, Website, Industry, AnnualRevenue, NumberOfEmployees,
               OwnerId, CreatedDate, LastModifiedDate
        FROM Account
    """
    if last_modified_after:
        soql += f" WHERE LastModifiedDate > {last_modified_after}"

    # Bulk API 2.0 for large volumes
    results = sf.bulk2.Account.query(soql, max_records=100000)

    # Write to S3 Bronze as JSON lines
    s3 = boto3.client('s3')
    batch_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    key = f'bronze/salesforce/account/batch_{batch_id}.json'

    s3.put_object(
        Bucket='company-mdm-lakehouse-prod',
        Key=key,
        Body=json.dumps(results),
        ServerSideEncryption='aws:kms',
    )
    print(f'Extracted {len(results)} accounts → s3://.../bronze/salesforce/account/')


# ═══════════════════════════════════════
# PATTERN 2: Real-time CDC (EventBridge)
# ═══════════════════════════════════════

def lambda_handler(event, context):
    """
    AWS Lambda handler for Salesforce CDC events.
    Triggered by EventBridge rule matching AccountChangeEvent.
    """
    s3 = boto3.client('s3')

    for record in event.get('detail', {}).get('payload', {}).get('ChangeEventHeader', []):
        change_type = record.get('changeType', 'UNKNOWN')
        entity_name = record.get('entityName', 'Account')
        record_ids = record.get('recordIds', [])

        cdc_payload = {
            'change_type': change_type,
            'entity_name': entity_name,
            'record_ids': record_ids,
            'changed_fields': record.get('changedFields', []),
            'commit_timestamp': record.get('commitTimestamp'),
            '_source_system': 'SALESFORCE_CDC',
            '_ingestion_ts': datetime.utcnow().isoformat(),
        }

        # Write CDC event to S3 Bronze
        ts = datetime.utcnow().strftime('%Y/%m/%d/%H')
        key = f'bronze/salesforce/cdc/{ts}/{record_ids[0] if record_ids else "unknown"}.json'

        s3.put_object(
            Bucket='company-mdm-lakehouse-prod',
            Key=key,
            Body=json.dumps(cdc_payload),
            ServerSideEncryption='aws:kms',
        )

    return {'statusCode': 200, 'body': f'Processed {len(event.get("detail", {}))} CDC events'}
