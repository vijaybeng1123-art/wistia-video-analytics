CREATE EXTERNAL TABLE IF NOT EXISTS wistia_analytics.dim_media (
    media_id string,
    media_name string,
    source_system string,
    created_at timestamp,
    updated_at timestamp
)
STORED AS PARQUET
LOCATION 's3://wistia-video-analytics-de/gold/dim_media/';
