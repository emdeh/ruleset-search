 # Define global settings here, such as Azure Storage connection strings (use environment variables for actual values to keep them secure).
# Responsible for loading the environment variables from your .env file and making them available as Python variables in your application
import os
from dotenv import load_dotenv

# Load directories from .env file
load_dotenv()
ruleset_path = os.getenv('RULESET_PATH')
input_dir = os.getenv('INPUT_DIR')
output_dir = os.getenv('OUTPUT_DIR')
output_csv_path = os.getenv('OUTPUT_CSV_PATH')
input_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))] 
original_path = os.getenv('ORIGINAL_PATH')

# Load configuration settings, such as Azure connection strings and container name

blob_account_url = os.getenv('ACCOUNT_URL')
blob_container_name = os.getenv('CONTIANER_NAME')
blob_credential = os.getenv('SAS_TOKEN')
blob_service_client = os.getenv('BLOB_SERVICE_CLIENT')