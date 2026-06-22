# Runbook

## Pipeline Jobs

The Glue workflow runs the jobs in this order:

1. wistia_ingestion_job
2. bronze_to_silver_job
3. silver_to_gold_job

## Manual Run

Go to AWS Glue > Workflows > wistia_analytics_workflow and click Run workflow.

## Scheduled Run

EventBridge Scheduler runs the Glue workflow daily for the 7-day production run.

## Validation

Use Athena to validate row counts:

SELECT
    engagement_date,
    COUNT(*) AS row_count
FROM wistia_analytics.fact_media_engagement
GROUP BY engagement_date
ORDER BY engagement_date;

