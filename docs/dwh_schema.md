# Data Warehouse Schema

## Overview

The Wistia Video Analytics data warehouse is built in the Gold layer of the S3 data lake and queried through Amazon Athena.

The model uses a dimensional warehouse design with fact and dimension tables.

## Athena Database

wistia_analytics

## Gold Tables

| Table | Table Type | Purpose |
|---|---|---|
| dim_media | Dimension | Stores Wistia media attributes |
| dim_visitor | Dimension | Stores visitor attributes |
| fact_media_engagement | Fact | Stores daily video engagement metrics |

---

## dim_media

### Purpose

The `dim_media` table stores descriptive information about each Wistia media item.

### Grain

One row per Wistia media ID.

### Columns

| Column | Description |
|---|---|
| media_id | Wistia media identifier |
| media_name | Friendly media name |
| source_system | Source system name |
| created_at | Record creation timestamp |
| updated_at | Record update timestamp |

### S3 Location

s3://wistia-video-analytics-de/gold/dim_media/

---

## dim_visitor

### Purpose

The `dim_visitor` table stores visitor descriptive attributes.

### Grain

One row per visitor ID.

### Current Implementation Note

The current Wistia media stats API pull provides aggregate visitor metrics, not detailed individual visitor records. Because of this, the pipeline creates a default visitor record with:

- visitor_id: unknown_visitor
- ip_address: NULL
- country: unknown

This keeps the dimensional model aligned with the project requirement and allows visitor-level enrichment to be added later.

### Columns

| Column | Description |
|---|---|
| visitor_id | Visitor identifier |
| ip_address | Visitor IP address |
| country | Visitor country |
| source_system | Source system name |
| created_at | Record creation timestamp |
| updated_at | Record update timestamp |

### S3 Location

s3://wistia-video-analytics-de/gold/dim_visitor/

---

## fact_media_engagement

### Purpose

The `fact_media_engagement` table stores daily Wistia video engagement metrics.

### Grain

One row per media ID per engagement date.

### Columns

| Column | Description |
|---|---|
| media_id | Wistia media identifier |
| engagement_date | Engagement metric date |
| load_count | Number of video loads |
| play_count | Number of video plays |
| play_rate | Ratio of plays to loads |
| hours_watched | Total hours watched |
| engagement | Wistia engagement metric |
| visitor_count | Aggregate number of visitors |
| ingested_at | Bronze ingestion timestamp |
| silver_processed_at | Silver processing timestamp |
| gold_processed_at | Gold processing timestamp |
| source_system | Source system name |

### S3 Location

s3://wistia-video-analytics-de/gold/fact_media_engagement/

---

## Relationship Model

Current join relationship:

fact_media_engagement.media_id joins to dim_media.media_id.

The dim_visitor table is included as a required dimension table. Since current Wistia stats are aggregate-level, visitor_count is stored in the fact table and dim_visitor currently contains a default visitor record.
