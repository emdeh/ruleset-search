 # Define global settings here, such as Azure Storage connection strings (use environment variables for actual values to keep them secure).

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

# connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
# container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')