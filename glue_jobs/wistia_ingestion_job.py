import json
import boto3
import requests
import traceback
from datetime import datetime, timezone

S3_BUCKET = "wistia-video-analytics-de"
SECRET_NAME = "wistia/api-token"
AWS_REGION = "us-east-1"

MEDIA_IDS = ["8hunphufxp", "9k4tbcdfg0"]

s3 = boto3.client("s3", region_name=AWS_REGION)
secrets = boto3.client("secretsmanager", region_name=AWS_REGION)


def now_utc():
    return datetime.now(timezone.utc)


def run_date():
    return now_utc().date().isoformat()


def write_s3(key, data):
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(data, indent=2, default=str),
        ContentType="application/json"
    )
    print(f"WROTE: s3://{S3_BUCKET}/{key}")


def get_token():
    secret_response = secrets.get_secret_value(SecretId=SECRET_NAME)
    secret_json = json.loads(secret_response["SecretString"])
    token = secret_json.get("WISTIA_API_TOKEN")

    if not token:
        raise Exception("WISTIA_API_TOKEN key not found in Secrets Manager secret.")

    return token


def call_wistia_media_stats(media_id, token):
    url = f"https://api.wistia.com/v1/stats/medias/{media_id}.json"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    print(f"Calling Wistia API for media_id={media_id}")

    response = requests.get(url, headers=headers, timeout=30)

    print(f"media_id={media_id}, status_code={response.status_code}")

    output = {
        "media_id": media_id,
        "endpoint": url,
        "status_code": response.status_code,
        "ingested_at": now_utc().isoformat(),
        "response_text": response.text
    }

    try:
        output["response_json"] = response.json()
    except Exception:
        output["response_json"] = None

    if response.status_code != 200:
        raise Exception(
            f"Wistia API failed for media_id={media_id}. "
            f"Status={response.status_code}, Body={response.text}"
        )

    return output


def main():
    print("WISTIA BRONZE INGESTION STARTED")

    started_at = now_utc().isoformat()
    today = run_date()
    files_written = []

    try:
        token = get_token()

        for media_id in MEDIA_IDS:
            result = call_wistia_media_stats(media_id, token)

            bronze_key = (
                f"bronze/media_stats/"
                f"run_date={today}/"
                f"media_id={media_id}/"
                f"data.json"
            )

            write_s3(bronze_key, result)
            files_written.append(bronze_key)

        success_log = {
            "job_name": "wistia_ingestion_job",
            "status": "success",
            "run_date": today,
            "started_at": started_at,
            "completed_at": now_utc().isoformat(),
            "media_ids": MEDIA_IDS,
            "files_written": files_written,
            "file_count": len(files_written)
        }

        write_s3(
            f"logs/run_date={today}/ingestion_log.json",
            success_log
        )

        state = {
            "last_successful_run": today,
            "status": "active",
            "updated_at": now_utc().isoformat()
        }

        write_s3("state/pipeline_state.json", state)

        print("WISTIA BRONZE INGESTION FINISHED SUCCESSFULLY")

    except Exception as e:
        error_log = {
            "job_name": "wistia_ingestion_job",
            "status": "failed",
            "run_date": today,
            "started_at": started_at,
            "failed_at": now_utc().isoformat(),
            "error": str(e),
            "traceback": traceback.format_exc(),
            "files_written_before_failure": files_written
        }

        write_s3(
            f"logs/run_date={today}/ingestion_failed.json",
            error_log
        )

        print("WISTIA BRONZE INGESTION FAILED")
        print(str(e))
        raise


if __name__ == "__main__":
    main()