# Local Deployment & gcloud CLI

## gcloud CLI
In this markdown, I touch on local deployment of the job, as well has making use of the [gcloud CLI](https://cloud.google.com/sdk/gcloud). This is necessary later on, but not for our local job.

Make sure to install the gcloud CLI [here](https://cloud.google.com/sdk/docs/install).

Then, initialize the CLI:

```bash
gcloud init
```

Follow the resulting pop-up in your browser to sign in to your account. You may also set it to  your desired project:

```bash
gcloud config set project PROJECT_ID
```

***

## Local deployment

### Obtaining a key

This step is for local deployment before our cloud deployment. Here, we do not require the gcloud CLI, unless you wish to obtain a service account key from the CLI (you may opt to do it from the console instead). This service account key is [needed](https://cloud.google.com/docs/authentication/application-default-credentials#GAC) for our local job to load the data into our BigQuery tables.

obtain key via CLI:

```bash
gcloud iam service-accounts keys create KEY_FILE \
    --iam-account=SA_NAME@PROJECT_ID.iam.gserviceaccount.com
```

where:\
`KEY_FILE` is the path to the downloaded key file on your machine; \
`SA_NAME` is your service account name, while \
`PROJECT_ID` is the ID of your project. <br><br>

Upon key creation: you should be able to see this:

![service-key](/docs/images/service-key.png) <br><br>

Finally, simply add the key file to your env. file, with the variable `GOOGLE_CREDENTIALS_PATH`. In our [`docker-compose.yaml`](/job/docker-compose.yaml), this is mounted and accessed by the container as `GOOGLE_APPLICATION_CREDENTIALS`, which the `bigquery` library uses in [`bigquery_loader.py`](/job/bigquery_loader.py).<br><br>

### Local Job Run

First, we navigate to our `job` directory:

```
cd job
```
Then, simply run:

```bash
docker compose up
```

This is what you should see upon successful job run:

![local-job-run-logs](/docs/images/local-job-run-logs.png)



