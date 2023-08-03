from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.hooks.mysql_hook import MySqlHook
import pickle
import logging
import pandas as pd
from tqdm import tqdm
from utils.scraper import scrape_data_from_url

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

def extract_data():
    file_path = 'dags/data/urls_list.pkl'

    # Load the list from the file using pickle.load()
    with open(file_path, 'rb') as f:
        url_list = pickle.load(f)

    logger.info(f"URLs are loaded. The length is: {len(url_list)}")
    return url_list

def transform_data(url_list):
    data_list = []
    for url in tqdm(url_list[:10], desc="Scraping Progress"):
        data_list.append(scrape_data_from_url(url))

    df = pd.DataFrame(data_list)
    df.to_csv('dags/data/scraped_data.csv', index=False)

    logger.info("Data is scraped and saved as a CSV file.")
    return 'dags/data/scraped_data.csv'

def check_data_availability(csv_file_path):
    df = pd.read_csv(csv_file_path)
    if df.empty:
        logger.info("Transformed data is empty. Ending the DAG run.")
        return 'no_data_to_load'
    else:
        logger.info("Transformed data is available. Proceeding to load data.")
        return 'load_data'

def load_data(csv_file_path):
    # # Connect to MySQL database
    # mysql_conn_id = 'mysql_conn'  # Update this with your MySQL connection ID in Airflow
    # mysql_hook = MySqlHook(mysql_conn_id=mysql_conn_id)

    # # Read the transformed data from the CSV file
    # df = pd.read_csv(csv_file_path)

    # Load data into MySQL database table
    table_name = 'scraped table'  # Update this with your desired table name
    # mysql_hook.insert_rows(table=table_name, rows=df.values.tolist(), target_fields=df.columns.tolist())

    logger.info(f"Data loaded into table '{table_name}' in the MySQL database.")

def no_data_to_load():
    logger.info("There is no data to load. Ending the DAG run.")

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