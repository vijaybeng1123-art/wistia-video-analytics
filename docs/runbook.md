# Runbook

## Pipeline Overview

The Wistia Video Analytics Pipeline extracts data from the Wistia Stats API, stores raw data in S3 Bronze, transforms it to Silver Parquet, and builds Gold dimensional warehouse tables for Athena querying.

## Pipeline Jobs

The AWS Glue Workflow runs the jobs in this order:

1. wistia_ingestion_job
2. bronze_to_silver_job
3. silver_to_gold_job

## Manual Pipeline Run

1. Open AWS Glue.
2. Go to Workflows.
3. Select wistia_analytics_workflow.
4. Click Run.
5. Wait for all jobs to complete successfully.
6. Open Athena and validate the Gold tables.

## Scheduled Pipeline Run

Amazon EventBridge Scheduler starts the Glue workflow daily during the 7-day production run.

## Gold Tables to Validate

The Gold layer should contain:

1. dim_media
2. dim_visitor
3. fact_media_engagement

## Validate dim_media

Run in Athena:

SELECT *
FROM wistia_analytics.dim_media;

Expected:

Two rows, one per Wistia media ID.

## Validate dim_visitor

Run in Athena:

SELECT *
FROM wistia_analytics.dim_visitor;

Expected current result:

visitor_id = unknown_visitor
ip_address = NULL
country = unknown
source_system = wistia

## Validate fact_media_engagement

Run in Athena:

SELECT *
FROM wistia_analytics.fact_media_engagement
ORDER BY engagement_date DESC, media_id;

Expected:

Rows by engagement date and media ID.

## Validate Fact Row Counts by Date

Run in Athena:

SELECT
    engagement_date,
    COUNT(*) AS row_count
FROM wistia_analytics.fact_media_engagement
GROUP BY engagement_date
ORDER BY engagement_date;

Expected:

Each completed run date should have 2 rows, one for each Wistia media ID.

For a full 7-day production run:

7 days x 2 media IDs = 14 fact rows.

## Validate Media Star Schema Join

Run in Athena:

SELECT
    f.engagement_date,
    m.media_name,
    f.load_count,
    f.play_count,
    f.play_rate,
    f.hours_watched,
    f.visitor_count
FROM wistia_analytics.fact_media_engagement f
JOIN wistia_analytics.dim_media m
    ON f.media_id = m.media_id
ORDER BY f.engagement_date DESC, m.media_name;

## Troubleshooting

### Glue Workflow Fails

Check the failed job in AWS Glue and review the CloudWatch logs.

### Athena Table Shows No Data

Confirm that the matching S3 Gold path contains Parquet files.

Expected locations:

s3://wistia-video-analytics-de/gold/dim_media/
s3://wistia-video-analytics-de/gold/dim_visitor/
s3://wistia-video-analytics-de/gold/fact_media_engagement/

### dim_visitor Missing

Confirm that the updated silver_to_gold_job.py has been uploaded to S3:

s3://wistia-video-analytics-de/scripts/glue_jobs/silver_to_gold_job.py

Then rerun the Glue workflow and recreate the Athena table if needed.
