from google.cloud import bigquery
from typing import List, Dict
from schemas import POSTS_SCHEMA, COMMENTS_SCHEMA, INSIGHTS_SCHEMA

class BigQueryLoader:
    def __init__(self, project_dataset: str):
        self.client = bigquery.Client()
        self.project_dataset = project_dataset

    def load_posts(self, posts: List[Dict]) -> int:
        """Load posts into BigQuery"""
        table_id = f"{self.project_dataset}.posts"
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            schema=POSTS_SCHEMA
        )

        job = self.client.load_table_from_json(
            posts,
            table_id,
            job_config=job_config
        )
        job.result()

        self.client.query(f'''
        ALTER TABLE `{table_id}`
        ADD PRIMARY KEY(post_id)
        NOT ENFORCED;
        ''')
        return job.output_rows

    def load_comments(self, comments: List[Dict]) -> int:
        """Load comments into BigQuery"""
        table_id = f"{self.project_dataset}.comments"
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            schema=COMMENTS_SCHEMA
        )

        job = self.client.load_table_from_json(
            comments,
            table_id,
            job_config=job_config
        )
        job.result()

        self.client.query(f'''
        ALTER TABLE `{table_id}`
        ADD PRIMARY KEY(comment_id)
        NOT ENFORCED;
        ''')
        return job.output_rows

    def load_insights(self, insights: List[Dict]) -> int:
        """Load insights into BigQuery"""
        table_id = f"{self.project_dataset}.insights"
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            schema=INSIGHTS_SCHEMA
        )

        job = self.client.load_table_from_json(
            insights,
            table_id,
            job_config=job_config
        )
        job.result()

        self.client.query(f'''
        ALTER TABLE `{table_id}`
        ADD PRIMARY KEY(post_id)
        NOT ENFORCED;
        ''')
        return job.output_rows

