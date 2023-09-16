import pickle
import logging
from tqdm import tqdm
import pandas as pd
from utils.scraper import scrape_data_from_url

logger = logging.getLogger(__name__)

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
