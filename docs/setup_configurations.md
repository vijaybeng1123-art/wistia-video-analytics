# Setup Configurations

## Project Name

Wistia Video Analytics Pipeline

## AWS Region

us-east-1

## S3 Bucket

wistia-video-analytics-de

## S3 Folder Structure

| Folder | Purpose |
|---|---|
| bronze/ | Raw JSON data extracted from the Wistia Stats API |
| silver/ | Cleaned and standardized Parquet data |
| gold/ | Final analytics-ready dimensional warehouse tables |
| logs/ | Pipeline logs and ingestion run details |
| scripts/ | AWS Glue job scripts |
| state/ | Incremental state and run metadata |
| athena-results/ | Athena query output location |

## AWS Glue Jobs

| Job Name | Job Type | Purpose |
|---|---|---|
| wistia_ingestion_job | Python Shell | Extracts Wistia API data and writes raw JSON to Bronze |
| bronze_to_silver_job | Spark | Cleans and standardizes Bronze data into Silver Parquet |
| silver_to_gold_job | Spark | Builds Gold dimensional warehouse tables |

## Glue Workflow

Workflow name:

wistia_analytics_workflow

Workflow order:

1. wistia_ingestion_job
2. bronze_to_silver_job
3. silver_to_gold_job

## EventBridge Scheduler

The pipeline is scheduled using Amazon EventBridge Scheduler.

The scheduler starts the AWS Glue Workflow daily during the production run window.

## Secrets Manager

Secret name:

wistia/api-token

Expected format:

{
  "WISTIA_API_TOKEN": "your_token_here"
}

The Wistia API token should never be hardcoded in source code or committed to GitHub.

## Athena Database

Database name:

wistia_analytics

## Athena Tables

| Table | Type | Purpose |
|---|---|---|
| dim_media | Dimension | Stores Wistia media attributes |
| dim_visitor | Dimension | Stores visitor attributes |
| fact_media_engagement | Fact | Stores daily video engagement metrics |

## GitHub Repository

Repository:

wistia-video-analytics

## CI/CD

GitHub Actions is used for CI/CD validation.

Workflow file:

.github/workflows/validate.yml

The workflow validates required project files and confirms that SQL files are populated.
