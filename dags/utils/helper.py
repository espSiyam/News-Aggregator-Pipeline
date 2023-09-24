import pickle
import logging
from tqdm import tqdm
import pandas as pd
from utils.scraper import scrape_data_from_url

FILE_PATH = 'dags/data/urls_list.pkl'
PROTHOM_ALO_URL_LIST = "dags/data/prothomalo_urls_list.pkl"
JUGANTOR_URL_LIST = "dags/data/jugantor_urls_list.pkl"
KALER_KANTHO_URL_LIST = "dags/data/kalerkantho_urls_list.pkl"
TRANSFORMED_DATA_CSV = "dags/data/scraped_data.csv"

logger = logging.getLogger(__name__)

def load_pkls(path):
    try:
        with open(path, 'rb') as f:
            url_list = pickle.load(f)
        return url_list
    except Exception as e:
        logger.error(f"Could not load data due to error: {str(e)} for path: {path}")

def extract_data():
    with open(FILE_PATH, 'rb') as f:
        url_list = pickle.load(f)

    logger.info(f"URLs are loaded. The length is: {len(url_list)}")
    return url_list

def transform_data():
    try:
        prothomalo_urls = load_pkls(PROTHOM_ALO_URL_LIST)
        jugantor_urls = load_pkls(JUGANTOR_URL_LIST)
        kalerkantho_urls = load_pkls(KALER_KANTHO_URL_LIST)

        # Combine the data from three sources into a single list
        combined_data = prothomalo_urls + jugantor_urls + kalerkantho_urls

        data_list = []
        for url in tqdm(combined_data[:10], desc="Scraping Progress"):
            data_list.append(scrape_data_from_url(url))

        df = pd.DataFrame(data_list)
        df.to_csv(TRANSFORMED_DATA_CSV, index=False)
        logger.info("Data is scraped and saved as a CSV file.")
    
    except Exception as e:
        logger.error(f"Could not transform data due to error: {str(e)}")

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