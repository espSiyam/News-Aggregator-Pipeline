import pickle
import logging
from tqdm import tqdm
import pandas as pd
from utils.scraper import scrape_data_from_url
from google.cloud import storage
import os
from datetime import datetime

FILE_PATH = 'dags/data/urls_list.pkl'
PROTHOM_ALO_URL_LIST = "dags/data/prothomalo_urls_list.pkl"
JUGANTOR_URL_LIST = "dags/data/jugantor_urls_list.pkl"
KALER_KANTHO_URL_LIST = "dags/data/kalerkantho_urls_list.pkl"
date = datetime.now().strftime("%Y-%m-%d")
TRANSFORMED_DATA_CSV = f"dags/data/scraped_data_{date}.csv"
GCP_PROJECT_ID = 'concured-playground'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dags/utils/news_gcp_project.json"

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
        numbers_of_urls_to_scrape = None
        if numbers_of_urls_to_scrape:
            if numbers_of_urls_to_scrape > len(combined_data):
                numbers_of_urls_to_scrape = len(combined_data)
            for url in tqdm(combined_data[:numbers_of_urls_to_scrape], desc="Scraping Progress"):
                data_list.append(scrape_data_from_url(url))
        else:
            for url in tqdm(combined_data, desc="Scraping Progress"):
                data_list.append(scrape_data_from_url(url))

        df = pd.DataFrame(data_list)
        df.to_csv(TRANSFORMED_DATA_CSV, index=False)
        logger.info("Data is scraped and saved as a CSV file.")
    
    except Exception as e:
        logger.error(f"Could not transform data due to error: {str(e)}")
        raise Exception(f"Could not transform data due to error: {str(e)}")

def load_to_gcp():
    storage_client = storage.Client(project=GCP_PROJECT_ID)

    bucket_name = 'sementic_assignment'  
    file_name = 'news_data.csv'
    local_file_path = TRANSFORMED_DATA_CSV

    # Upload the local file to GCS
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(local_file_path)

    logger.info(f"File {file_name} uploaded to {bucket_name} successfully!")
    