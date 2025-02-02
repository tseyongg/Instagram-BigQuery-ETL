from airflow import DAG
from airflow.providers.google.cloud.operators.cloud_run import CloudRunExecuteJobOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
from pendulum import timezone

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email': ['leannefoolx@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'execution_timeout': timedelta(minutes=30),
    'depends_on_past': False,
}

dag = DAG(
    'instagram_collector_job',
    default_args=default_args,
    description='Test DAG for Instagram collection with email notification',
    schedule_interval='0 */6 * * *',
    start_date=datetime(2025, 1, 1, tzinfo=timezone('Asia/Singapore')),
    catchup=False,
    tags=['instagram', 'cloud_run'],
    max_active_runs=1
)

collect_instagram = CloudRunExecuteJobOperator(
    task_id='collect_instagram_data',
    project_id='winged-yeti-440908-r9',
    region='asia-southeast1',
    job_name='instagram-collector-job',
    deferrable=True,
    dag=dag,
)

send_success_email = EmailOperator(
   task_id='send_success_email',
   to=['leannefoolx@gmail.com'],
   subject='Instagram Data Collection Success',
   html_content="""
   <h3>Instagram Data Collection Completed Successfully</h3>
   <p>The data collection process has finished successfully.</p>
   
   <p>Collection Time Taken: {{ (task_instance.get_dagrun().get_task_instance('collect_instagram_data').duration / 60)|int }} minutes and {{ (task_instance.get_dagrun().get_task_instance('collect_instagram_data').duration % 60)|int }} seconds</p>
   """,
   dag=dag
)

# Set task dependencies
collect_instagram >> send_success_email