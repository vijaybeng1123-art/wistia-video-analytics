# Data Dictionary

## dim_media

| Column | Description |
|---|---|
| media_id | Wistia media identifier |
| media_name | Friendly media name |
| source_system | Source system name |
| created_at | Dimension record creation timestamp |
| updated_at | Dimension record update timestamp |

## fact_media_engagement

| Column | Description |
|---|---|
| media_id | Wistia media identifier |
| engagement_date | Date of the engagement metrics |
| load_count | Number of video loads |
| play_count | Number of video plays |
| play_rate | Percentage of loads that became plays |
| hours_watched | Total hours watched |
| engagement | Wistia engagement metric |
| visitor_count | Number of visitors |
| ingested_at | Bronze ingestion timestamp |
| silver_processed_at | Silver transformation timestamp |
| gold_processed_at | Gold transformation timestamp |
| source_system | Source system name |
