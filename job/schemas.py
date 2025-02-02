from google.cloud import bigquery

POSTS_SCHEMA = [
    bigquery.SchemaField("post_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("caption", "STRING"),
    bigquery.SchemaField("media_type", "STRING"),
    bigquery.SchemaField("post_timestamp", "DATETIME"),
    bigquery.SchemaField("post_like_count", "INTEGER"),
    bigquery.SchemaField("comments_count", "INTEGER"),
    bigquery.SchemaField("permalink", "STRING"),
    bigquery.SchemaField("post_collected_at", "DATETIME"),
]

COMMENTS_SCHEMA = [
    bigquery.SchemaField("comment_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("postid", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("comment_text", "STRING"),
    bigquery.SchemaField("comment_timestamp", "DATETIME"),
    bigquery.SchemaField("username", "STRING"),
    bigquery.SchemaField("comment_like_count", "INTEGER"),
    bigquery.SchemaField("comment_collected_at", "DATETIME"),
]

INSIGHTS_SCHEMA = [
    bigquery.SchemaField("post_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("impressions", "INTEGER"),
    bigquery.SchemaField("profile_visits", "INTEGER"),
    bigquery.SchemaField("reach", "INTEGER"),
    bigquery.SchemaField("shares", "INTEGER"),
    bigquery.SchemaField("saved", "INTEGER"),
    bigquery.SchemaField("plays", "INTEGER"),
    bigquery.SchemaField("ig_reels_avg_watch_time", "FLOAT"),
    bigquery.SchemaField("insights_collected_at", "DATETIME"),
]