from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.hooks.mysql_hook import MySqlHook
import pickle
import logging
import pandas as pd
from tqdm import tqdm
from utils.scraper import scrape_data_from_url
from utils.helper import extract_data, transform_data, check_data_availability, load_data, no_data_to_load

logger = logging.getLogger(__name__)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 7, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ETL_Pipeline',
    default_args=default_args,
    schedule_interval='*/60 * * * *',  # Execute every minute
    catchup=False
)

# Define the tasks
task_extract_data = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

task_transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    op_args=[task_extract_data.output],
    dag=dag
)

task_check_data_availability = BranchPythonOperator(
    task_id='check_data_availability',
    python_callable=check_data_availability,
    op_args=[task_transform_data.output],
    dag=dag
)

task_load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    op_args=[task_transform_data.output],
    dag=dag
)

task_no_data_to_load = PythonOperator(
    task_id='no_data_to_load',
    python_callable=no_data_to_load,
    dag=dag
)

# Define the DAG's execution flow
task_extract_data >> task_transform_data >> task_check_data_availability
task_check_data_availability >> task_load_data
task_check_data_availability >> task_no_data_to_load