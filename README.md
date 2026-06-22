# Wistia Video Analytics Pipeline

This project builds an end-to-end AWS data pipeline for Wistia video analytics.

## Architecture

Wistia Stats API data is ingested into Amazon S3 using AWS Glue Python Shell, transformed through Bronze, Silver, and Gold layers using AWS Glue Spark jobs, and queried through Athena as a serverless data warehouse.

## Pipeline Flow

Wistia API → S3 Bronze → S3 Silver → S3 Gold → Glue Data Catalog → Athena

## AWS Services Used

- AWS Glue
- Amazon S3
- AWS Secrets Manager
- Amazon Athena
- Amazon EventBridge Scheduler
- AWS IAM
- GitHub Actions

## Data Warehouse Model

Database: wistia_analytics

Tables:

- dim_media
- fact_media_engagement

## Workflow

The Glue workflow runs these jobs in order:

1. wistia_ingestion_job
2. bronze_to_silver_job
3. silver_to_gold_job

## Validation

Athena queries are stored in the athena folder.
