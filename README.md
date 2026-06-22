# Wistia Video Analytics Pipeline

## Project Overview

This project builds an end-to-end AWS data engineering pipeline for Wistia video analytics. The pipeline extracts video performance data from the Wistia Stats API, stores raw data in Amazon S3, transforms the data through Bronze, Silver, and Gold layers using AWS Glue, and exposes a serverless data warehouse through Amazon Athena.

## Architecture

Wistia Stats API → AWS Glue Python Shell → S3 Bronze → AWS Glue Spark → S3 Silver → AWS Glue Spark → S3 Gold → Glue Data Catalog → Athena

## AWS Services Used

- Amazon S3
- AWS Glue
- AWS Glue Workflow
- AWS Secrets Manager
- Amazon Athena
- Amazon EventBridge Scheduler
- AWS IAM
- GitHub Actions

## S3 Bucket

Bucket:

wistia-video-analytics-de
S3 Data Lake Structure

The project uses an S3-based data lake with the following folder structure:

bronze/
silver/
gold/
logs/
scripts/
state/
athena-results/
Folder Purpose
Folder	Purpose
bronze/	Stores raw JSON data extracted from the Wistia Stats API
silver/	Stores cleaned and standardized Parquet data
gold/	Stores final analytics-ready dimensional warehouse tables
logs/	Stores ingestion logs and pipeline run details
scripts/	Stores Glue job scripts used by the pipeline
state/	Stores incremental pipeline state, such as last run metadata
athena-results/	Stores Athena query output results
Pipeline Layers
Bronze Layer

The Bronze layer stores raw API responses from the Wistia Stats API.

Example path:

s3://wistia-video-analytics-de/bronze/media_stats/
Silver Layer

The Silver layer stores cleaned and standardized data in Parquet format.

Example path:

s3://wistia-video-analytics-de/silver/media_stats/
Gold Layer

The Gold layer stores analytics-ready dimensional warehouse tables.

Example paths:

s3://wistia-video-analytics-de/gold/dim_media/
s3://wistia-video-analytics-de/gold/fact_media_engagement/
Glue Jobs

The pipeline contains three main AWS Glue jobs:

wistia_ingestion_job
bronze_to_silver_job
silver_to_gold_job
wistia_ingestion_job

This AWS Glue Python Shell job extracts video analytics data from the Wistia Stats API and writes raw JSON data to the Bronze layer in Amazon S3.

bronze_to_silver_job

This AWS Glue Spark job reads raw Bronze data, cleans and standardizes the fields, and writes the output to the Silver layer in Parquet format.

silver_to_gold_job

This AWS Glue Spark job reads the Silver layer and creates the Gold dimensional warehouse tables used for Athena reporting.

Glue Workflow

Workflow name:

wistia_analytics_workflow

The AWS Glue Workflow runs the jobs in this order:

start_wistia_ingestion
        ↓
wistia_ingestion_job
        ↓
run_bronze_to_silver_after_ingestion
        ↓
bronze_to_silver_job
        ↓
run_silver_to_gold_after_bronze
        ↓
silver_to_gold_job
Scheduling

The pipeline is scheduled using Amazon EventBridge Scheduler.

The scheduler starts the Glue workflow daily during the 7-day production run.

Athena Data Warehouse

Athena database:

wistia_analytics

Gold tables:

dim_media
fact_media_engagement
Dimensional Model
dim_media

The dim_media table stores media-level descriptive information.

Grain:

One row per Wistia media ID
fact_media_engagement

The fact_media_engagement table stores daily media engagement metrics.

Grain:

One row per media ID per engagement date
Validation Query

Use Athena to validate the final fact table row count:

SELECT
    engagement_date,
    COUNT(*) AS row_count
FROM wistia_analytics.fact_media_engagement
GROUP BY engagement_date
ORDER BY engagement_date;

Expected result for the 7-day production run:

7 days x 2 videos = 14 fact rows
CI/CD

GitHub Actions validates the project on every push to the main branch.

The validation workflow checks that required project files exist and that SQL files are populated.

Workflow file:

.github/workflows/validate.yml
Security

The Wistia API token is not stored in the GitHub repository.

The token is stored securely in AWS Secrets Manager.

Secret name:

wistia/api-token
