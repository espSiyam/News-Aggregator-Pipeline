# from google.cloud import storage

# # Specify your GCP project ID
# project_id = 'concured-playground'

# # Authenticate with GCP using the environment variable
# storage_client = storage.Client(project=project_id)

# # Define your GCS bucket and file name
# bucket_name = 'etl_pipeline_practice'  # Replace with your GCS bucket name
# file_name = 'test.ipynb'  # Replace with your local file name
# # Specify the path to your local file
# local_file_path = 'test.ipynb'

# # Upload the file to GCS
# bucket = storage_client.bucket(bucket_name)
# blob = bucket.blob(file_name)
# blob.upload_from_filename(local_file_path)

# print(f"File {file_name} uploaded to {bucket_name} successfully!")



# Part 2 
import os
from google.cloud import storage

GCP_PROJECT_ID = 'concured-playground'
json_key_path = "/home/siyam/Documents/concured-playground-3e0db480e82a.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_key_path
storage_client = storage.Client(project=GCP_PROJECT_ID)

bucket_name = 'etl_pipeline_practice'  
file_name = 'news_data.csv'
local_file_path = 'dags/data/scraped_data.csv'

# Upload the local file to GCS
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(file_name)
blob.upload_from_filename(local_file_path)

print(f"File {file_name} uploaded to {bucket_name} successfully!")