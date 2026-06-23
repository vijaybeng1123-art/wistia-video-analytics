CREATE EXTERNAL TABLE IF NOT EXISTS wistia_analytics.dim_visitor (
    visitor_id string,
    ip_address string,
    country string,
    source_system string,
    created_at timestamp,
    updated_at timestamp
)
STORED AS PARQUET
LOCATION 's3://wistia-video-analytics-de/gold/dim_visitor/';
