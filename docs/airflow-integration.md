# Airflow Integration

## Environment  Creation

Begin by creating a [cloud composer environment](https://cloud.google.com/composer/docs/composer-3/create-environments). You may also specify configurations for your scheduler, web server, and workers, among others. Make sure to give it an `ENVIRONMENT_NAME` too. Below is what it should look like upon creation, mine has the `ENVIRONMENT_NAME`= "instagram-collector-composer-3" :

![composer-env-overview](/docs/images/composer-env-overview.png)

## Email SMTP Configuration

In our [DAG](/airflow/dags/airflow_job.py), our second task after running the job is to send an email on success. But this requires a configuration to be set up in the `airflow.cfg` file, and a few other steps. Otherwise, the email will not be able to be sent.

1. Firstly, we have to obtain an [app password](https://support.google.com/accounts/answer/185833) for out Google account in order for Airflow to be able to access the email account we will be sending from. An example of mine:

![google-app-pw](/docs/images/google-app-pw.png) <br><br>

2. Now you will need to create an email connection `smtp_default`, as detailed [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html). This is where you will input your user (gmail username) and password (app password). Below is how it should look like:

![smtp-default-conn](/docs/images/smtp-default-conn.png) <br><br>

3. Finally, you will need to override the configurations in the `airflow.cfg` file. You may do so in the console or in the [command line](https://cloud.google.com/composer/docs/composer-3/override-airflow-configurations). Use the following key-value pairs:

![airflow-cfg-overrides](/docs/images/airflow-cfg-overrides.png)

## Dag Run

Now, proceed to upload your [DAG](/airflow/dags/airflow_job.py) into your environment's cloud storage bucket:

```bash
gcloud composer environments storage dags import \
    --environment instagram-collector-composer-3 \
    --location asia-southeast1 \
    --source="LOCAL_FILE_TO_UPLOAD"
```

On completion, you should see your composer bucket update with your airflow file:

![composer-bucket](/docs/images/composer-bucket.png)