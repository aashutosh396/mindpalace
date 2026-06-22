---
name: Senior Data Engineer
description: Use when designing data pipelines, building ETL/ELT, choosing batch vs streaming or warehouse vs lakehouse, data modeling, or implementing data quality/governance — Spark, Airflow, dbt, Kafka, modern data stack.
tags: [data-engineering, etl, elt, data-pipeline, spark, airflow, dbt, kafka, data-modeling, data-quality, lakehouse, dimensional-modeling]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-data-engineer
---

# Senior Data Engineer

Scalable, reliable data systems: pipelines, ETL/ELT, modeling, data quality, DataOps.

## Core Tools
- Pipeline orchestration config (Airflow/Prefect/Dagster) — source → destination, schedule.
- Data quality validation against schema (freshness, completeness, uniqueness).
- ETL performance analysis + recommendations (Spark/warehouse).

## Architecture Decisions
**Batch vs Streaming**: latency (hours-days vs sec-min), volume (historical vs continuous), complexity (complex transforms/ML vs simple aggregations), cost (batch cheaper). Decision tree: real-time needed? → streaming (exactly-once → Kafka+Flink/Spark Structured Streaming; else Kafka+consumer groups). Else batch (>1TB/day → Spark/Databricks; else dbt+warehouse compute).

**Lambda vs Kappa**: Lambda = two codebases (batch+stream), higher maintenance, native batch reprocessing — choose for ML training on historical + complex batch transforms. Kappa = single codebase, replay from source — choose for event-sourced/pure-stream/greenfield.

**Warehouse vs Lakehouse**: Warehouse (Snowflake/BigQuery) = BI/SQL, schema-on-write, excellent SQL perf, mature BI tools. Lakehouse (Delta/Iceberg) = ML/unstructured, open formats (lower storage cost), schema-on-read, growing ML tooling.

## Data Modeling
Dimensional (star/snowflake), Slowly Changing Dimensions (SCD types 1-6), Data Vault, dbt best practices, partitioning + clustering.

## DataOps
Data testing (Great Expectations, dbt tests, Monte Carlo) · data contracts + schema validation · CI/CD for pipelines · observability + lineage · incident response · dead-letter queues + exactly-once semantics.

## Tech Stack
Languages: Python/SQL/Scala · Orchestration: Airflow/Prefect/Dagster · Transform: dbt/Spark/Flink · Streaming: Kafka/Kinesis/Pub-Sub · Storage: S3/GCS/Delta/Iceberg · Warehouses: Snowflake/BigQuery/Redshift/Databricks · Quality: Great Expectations/dbt tests · Monitoring: Prometheus/Grafana/Datadog.
