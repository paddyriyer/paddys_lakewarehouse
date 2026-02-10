"""
Silver Layer Transformation
=============================
Bronze → Silver: Schema enforcement, deduplication, type casting, null handling.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, trim, upper, lower, regexp_replace, when, coalesce,
    row_number, current_timestamp, sha2, concat_ws
)
from pyspark.sql.window import Window


def transform_customer_silver():
    """Clean and conform customer records from all Bronze sources."""
    spark = SparkSession.builder.appName('silver-customer-transform').getOrCreate()

    # ── Load Bronze sources ──
    sap = spark.read.format('delta').load('s3://lakehouse/bronze/sap/kna1/')
    sfdc = spark.read.format('delta').load('s3://lakehouse/bronze/salesforce/account/')

    # ── Conform SAP to common schema ──
    sap_clean = sap.select(
        col('KUNNR').alias('source_id'),
        trim(upper(col('NAME1'))).alias('full_name'),
        lower(trim(col('SMTP_ADDR'))).alias('email'),
        regexp_replace('TELF1', r'[^0-9+]', '').alias('phone'),
        upper(trim(col('LAND1'))).alias('country'),
        trim(col('ORT01')).alias('city'),
        trim(col('STRAS')).alias('street_address'),
        col('_source_system'),
        col('_ingestion_ts'),
    )

    # ── Conform Salesforce ──
    sfdc_clean = sfdc.select(
        col('Id').alias('source_id'),
        trim(upper(col('Name'))).alias('full_name'),
        lower(trim(col('Email'))).alias('email') if 'Email' in sfdc.columns else col('Website').alias('email'),
        regexp_replace('Phone', r'[^0-9+]', '').alias('phone'),
        upper(trim(col('BillingCountry'))).alias('country'),
        trim(col('BillingCity')).alias('city'),
        trim(col('BillingStreet')).alias('street_address'),
        col('_source_system'),
        col('_ingestion_ts'),
    )

    # ── Union + deduplicate ──
    combined = sap_clean.unionByName(sfdc_clean, allowMissingColumns=True)

    # Deduplicate within each source (keep most recent ingestion)
    window = Window.partitionBy('source_id', '_source_system').orderBy(col('_ingestion_ts').desc())
    deduped = (combined
               .withColumn('_row_num', row_number().over(window))
               .filter(col('_row_num') == 1)
               .drop('_row_num'))

    # ── Add Silver metadata ──
    silver = (deduped
              .withColumn('_silver_ts', current_timestamp())
              .withColumn('_row_hash', sha2(concat_ws('|', *deduped.columns), 256)))

    # ── Write to Silver ──
    silver.write.format('delta').mode('overwrite') \
        .save('s3://lakehouse/silver/customer/customer_master/')

    print(f'Silver customer_master: {silver.count()} records')


if __name__ == '__main__':
    transform_customer_silver()
