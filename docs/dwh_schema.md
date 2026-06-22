# Data Warehouse Schema

The Wistia Analytics data warehouse uses a star schema.

## Database

wistia_analytics

## Dimension Tables

### dim_media

Stores media-level descriptive attributes.

Columns:
- media_id
- media_name
- source_system
- created_at
- updated_at

## Fact Tables

### fact_media_engagement

Stores daily engagement metrics by media.

Columns:
- media_id
- engagement_date
- load_count
- play_count
- play_rate
- hours_watched
- engagement
- visitor_count
- ingested_at
- silver_processed_at
- gold_processed_at
- source_system
