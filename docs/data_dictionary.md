# Data Dictionary

## Database

wistia_analytics

---

## dim_media

The `dim_media` table stores media-level descriptive attributes.

Grain:

One row per Wistia media ID.

| Column | Data Type | Description |
|---|---|---|
| media_id | string | Wistia media identifier |
| media_name | string | Friendly media name created from the Wistia media ID |
| source_system | string | Source system name, set to wistia |
| created_at | timestamp | Timestamp when the dimension record was created |
| updated_at | timestamp | Timestamp when the dimension record was updated |

---

## dim_visitor

The `dim_visitor` table stores visitor-level descriptive attributes.

Grain:

One row per visitor ID.

Current note:

The current Wistia media stats endpoint provides aggregate visitor counts, not detailed individual visitor records. A default `unknown_visitor` record is created so the dimensional model includes the required visitor dimension. This table can be enriched later if visitor-level API data is added.

| Column | Data Type | Description |
|---|---|---|
| visitor_id | string | Visitor identifier. Current default value is unknown_visitor |
| ip_address | string | Visitor IP address. Current value is NULL because the media stats endpoint is aggregate-level |
| country | string | Visitor country. Current default value is unknown |
| source_system | string | Source system name, set to wistia |
| created_at | timestamp | Timestamp when the dimension record was created |
| updated_at | timestamp | Timestamp when the dimension record was updated |

---

## fact_media_engagement

The `fact_media_engagement` table stores daily media engagement metrics.

Grain:

One row per media ID per engagement date.

| Column | Data Type | Description |
|---|---|---|
| media_id | string | Wistia media identifier |
| engagement_date | date | Date associated with the engagement metrics |
| load_count | bigint | Number of video loads |
| play_count | bigint | Number of video plays |
| play_rate | double | Ratio of video plays to video loads |
| hours_watched | double | Total hours watched |
| engagement | double | Wistia engagement metric |
| visitor_count | bigint | Aggregate number of visitors |
| ingested_at | timestamp | Timestamp when the data was ingested into Bronze |
| silver_processed_at | timestamp | Timestamp when the data was processed into Silver |
| gold_processed_at | timestamp | Timestamp when the data was processed into Gold |
| source_system | string | Source system name, set to wistia |
