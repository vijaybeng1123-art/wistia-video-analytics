-- Validate fact table row counts by engagement date
SELECT
    engagement_date,
    COUNT(*) AS row_count
FROM wistia_analytics.fact_media_engagement
GROUP BY engagement_date
ORDER BY engagement_date;

-- Validate media dimension
SELECT *
FROM wistia_analytics.dim_media;

-- Validate visitor dimension
SELECT *
FROM wistia_analytics.dim_visitor;

-- Validate star schema join with media dimension
SELECT
    f.engagement_date,
    d.media_name,
    f.load_count,
    f.play_count,
    f.play_rate,
    f.hours_watched,
    f.visitor_count
FROM wistia_analytics.fact_media_engagement f
JOIN wistia_analytics.dim_media d
    ON f.media_id = d.media_id
ORDER BY f.engagement_date DESC, d.media_name;
