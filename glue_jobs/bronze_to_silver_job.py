from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql.functions import (
    col,
    current_timestamp,
    input_file_name,
    regexp_extract,
    to_date
)

BRONZE_PATH = "s3://wistia-video-analytics-de/bronze/media_stats/"
SILVER_PATH = "s3://wistia-video-analytics-de/silver/media_stats/"
DEBUG_PATH = "s3://wistia-video-analytics-de/silver/debug/"

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

print("BRONZE TO SILVER JOB STARTED")

debug_df = spark.createDataFrame(
    [("Spark job started successfully",)],
    ["message"]
).withColumn("processed_at", current_timestamp())

debug_df.write.mode("overwrite").parquet(DEBUG_PATH)

print(f"Wrote debug output to: {DEBUG_PATH}")
print(f"Reading bronze data from: {BRONZE_PATH}")

df = (
    spark.read
    .option("recursiveFileLookup", "true")
    .option("multiline", "true")
    .json(BRONZE_PATH)
)

print("Bronze record count:")
print(df.count())

print("Bronze schema:")
df.printSchema()

print("Bronze sample:")
df.show(10, truncate=False)

silver_df = (
    df
    .select(
        col("media_id").cast("string").alias("media_id"),
        col("response_json.load_count").cast("long").alias("load_count"),
        col("response_json.play_count").cast("long").alias("play_count"),
        col("response_json.play_rate").cast("double").alias("play_rate"),
        col("response_json.hours_watched").cast("double").alias("hours_watched"),
        col("response_json.engagement").cast("double").alias("engagement"),
        col("response_json.visitors").cast("long").alias("visitors"),
        col("status_code").cast("int").alias("status_code"),
        col("ingested_at").cast("timestamp").alias("ingested_at"),
        input_file_name().alias("source_file")
    )
    .withColumn(
        "run_date_string",
        regexp_extract(col("source_file"), r"run_date=([0-9\\-]+)", 1)
    )
    .withColumn("run_date", to_date(col("run_date_string")))
    .withColumn("processed_at", current_timestamp())
)

print("Silver record count:")
print(silver_df.count())

print("Silver schema:")
silver_df.printSchema()

print("Silver sample:")
silver_df.show(10, truncate=False)

silver_df.write.mode("overwrite").parquet(SILVER_PATH)

print(f"Wrote silver data to: {SILVER_PATH}")
print("BRONZE TO SILVER JOB FINISHED SUCCESSFULLY")