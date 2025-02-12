# Airflow Integration

Begin by creating a [cloud composer environment](https://cloud.google.com/composer/docs/composer-3/create-environments). You may also specify configurations for your scheduler, web server, and workers, among others. Make sure to give it an `ENVIRONMENT_NAME` too. Below is what it should look like upon creation, mine has the `ENVIRONMENT_NAME`= "instagram-collector-composer-3" :

![composer-env-overview](/docs/images/composer-env-overview.png)

Then, proceed to upload your [DAG](/airflow/dags/airflow_job.py) into your environment's cloud storage bucket:

```bash
gcloud composer environments storage dags import \
    --environment instagram-collector-composer-3 \
    --location asia-southeast1 \
    --source="LOCAL_FILE_TO_UPLOAD"
```

On completion, you should see your composer bucket update with your dag:

![composer-bucket](/docs/images/composer-bucket.png)

