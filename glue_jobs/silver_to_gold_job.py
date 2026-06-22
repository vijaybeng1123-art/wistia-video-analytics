from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql.functions import (
    col,
    current_timestamp,
    lit,
    concat
)

# -----------------------------
# CONFIG
# -----------------------------

SILVER_PATH = "s3://wistia-video-analytics-de/silver/media_stats/"

GOLD_FACT_PATH = "s3://wistia-video-analytics-de/gold/fact_media_engagement/"
GOLD_DIM_MEDIA_PATH = "s3://wistia-video-analytics-de/gold/dim_media/"
GOLD_DEBUG_PATH = "s3://wistia-video-analytics-de/gold/debug/"

# -----------------------------
# SPARK SETUP
# -----------------------------

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

print("SILVER TO GOLD JOB STARTED")

# -----------------------------
# DEBUG WRITE
# -----------------------------

debug_df = spark.createDataFrame(
    [("Silver to gold job started successfully",)],
    ["message"]
).withColumn("processed_at", current_timestamp())

debug_df.write.mode("overwrite").parquet(GOLD_DEBUG_PATH)

print(f"Wrote debug output to: {GOLD_DEBUG_PATH}")

# -----------------------------
# READ SILVER
# -----------------------------

print(f"Reading silver data from: {SILVER_PATH}")

silver_df = spark.read.parquet(SILVER_PATH)

silver_count = silver_df.count()
print(f"Silver record count: {silver_count}")

if silver_count == 0:
    raise Exception("Silver table has 0 records. Cannot build gold DWH tables.")

print("Silver schema:")
silver_df.printSchema()

print("Silver sample:")
silver_df.show(10, truncate=False)

# -----------------------------
# BUILD DIMENSION TABLE: dim_media
# -----------------------------
# Note:
# Current Wistia stats endpoint gives media_id and metrics.
# We are creating a basic media dimension now.
# Later, if we ingest media metadata, we can add title, duration, upload_date, etc.

dim_media_df = (
    silver_df
    .select(
        col("media_id").cast("string").alias("media_id")
    )
    .dropDuplicates(["media_id"])
    .withColumn("media_name", concat(lit("Wistia Media "), col("media_id")))
    .withColumn("source_system", lit("wistia"))
    .withColumn("created_at", current_timestamp())
    .withColumn("updated_at", current_timestamp())
)

dim_count = dim_media_df.count()
print(f"Dim media record count: {dim_count}")

print("Dim media schema:")
dim_media_df.printSchema()

print("Dim media sample:")
dim_media_df.show(10, truncate=False)

# -----------------------------
# BUILD FACT TABLE: fact_media_engagement
# -----------------------------

fact_media_engagement_df = (
    silver_df
    .select(
        col("media_id").cast("string").alias("media_id"),
        col("run_date").cast("date").alias("engagement_date"),
        col("load_count").cast("long").alias("load_count"),
        col("play_count").cast("long").alias("play_count"),
        col("play_rate").cast("double").alias("play_rate"),
        col("hours_watched").cast("double").alias("hours_watched"),
        col("engagement").cast("double").alias("engagement"),
        col("visitors").cast("long").alias("visitor_count"),
        col("ingested_at").cast("timestamp").alias("ingested_at"),
        col("processed_at").cast("timestamp").alias("silver_processed_at")
    )
    .dropDuplicates(["media_id", "engagement_date"])
    .withColumn("gold_processed_at", current_timestamp())
    .withColumn("source_system", lit("wistia"))
)

fact_count = fact_media_engagement_df.count()
print(f"Fact media engagement record count: {fact_count}")

print("Fact media engagement schema:")
fact_media_engagement_df.printSchema()

print("Fact media engagement sample:")
fact_media_engagement_df.show(20, truncate=False)

# -----------------------------
# WRITE GOLD TABLES
# -----------------------------

print(f"Writing dim_media to: {GOLD_DIM_MEDIA_PATH}")

dim_media_df.write.mode("overwrite").parquet(GOLD_DIM_MEDIA_PATH)

print(f"Writing fact_media_engagement to: {GOLD_FACT_PATH}")

fact_media_engagement_df.write.mode("overwrite").parquet(GOLD_FACT_PATH)

print("SILVER TO GOLD JOB FINISHED SUCCESSFULLY")