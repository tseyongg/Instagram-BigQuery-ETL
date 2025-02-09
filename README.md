# Instagram ETL Pipeline
Data Pipeline for SISTIC Singapore, extracting data from Instagram API, transformed on Google Cloud Run, and finally loaded into Google BigQuery. 

## Motivation
This project was conceptualized to allow for easy analysis of SISTIC Singapore's Instagram posts, comments, and post insights.

It incorporates the developing of skills in the areas of API manipulation, Cloud technologies, and Orchestration tools.

## Architecture

![pipeline architecture](docs/images/architecture.png)

1. Extract Instagram data from Facebook Graph API
2. Containerized Cloud Run job transforms the data
3. Processed data is loaded into BigQuery
4. Orchestrated with Airflow on Composer, email is sent on successful job run

## Output

![output](docs/images/output_bq_tables.png)

Above is the output - three tables under the instagram_analytics dataset:
* Posts (PK: post_id)
* Insights (PK: post_id)
* Comments (PK: comment_id)

## Setup
Detailed setup instructions are available in the docs folder:
- [Instagram API Setup](docs/instagram-api-setup.md)
- [Cloud Composer Setup](docs/cloud-composer-setup.md)
- [Environment Variables](docs/environment-variables.md)
- [Authentication & Permissions](docs/authentication.md)
- [Airflow Email Task Configuration](docs/airflow-email-task-config.md)
- [Local & Cloud Development](docs/local-development.md)