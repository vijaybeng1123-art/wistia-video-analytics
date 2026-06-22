CREATE EXTERNAL TABLE IF NOT EXISTS wistia_analytics.fact_media_engagement (
    media_id string,
    engagement_date date,
    load_count bigint,
    play_count bigint,
    play_rate double,
    hours_watched double,
    engagement double,
    visitor_count bigint,
    ingested_at timestamp,
    silver_processed_at timestamp,
    gold_processed_at timestamp,
    source_system string
)
STORED AS PARQUET
LOCATION 's3://wistia-video-analytics-de/gold/fact_media_engagement/';
