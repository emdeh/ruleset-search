# Description: This script demonstrates how to process text from Azure Blob Storage and write the results to a CSV file.
import sys
import os
from text_processing import write_file_manifest, process_text, load_rulesets
from azure_blob_utils import get_blob_service_client, list_blobs, read_blob_content
import csv
import json # for testing

# Calculate the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root to the system path
sys.path.insert(0, project_root)

# import app_settings
from config import app_settings

def main():
    # Create manifest of input files
    write_file_manifest(app_settings.input_dir, app_settings.output_dir)

    # Initialize the Azure Blob Service Client
    blob_service_client = get_blob_service_client(app_settings.blob_account_url, app_settings.blob_credential)

    # Load the rulesets from a JSON file
    rulesets = load_rulesets(app_settings.ruleset_path)   

    # Prepare the CSV file for output
    with open(app_settings.output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Name', 'Triggered Rule', 'Triggered Condition', 'Path to File' 'Start', 'End'])

        '''
        # FOR TESTING #
        # Process the local JSON file
        for file_name in app_settings.input_files:
            file_path = os.path.join(app_settings.input_dir, file_name)
            clickable_path = app_settings.original_path + file_name
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                content = json.load(jsonfile)  # Assuming JSON format for simplicity
                text_content = content['text_content']  # Adjust based on actual content structure
                
                # Process the text content
                extracted_info = process_text(text_content, rulesets)
                for match in extracted_info:
                    csvwriter.writerow([
                        file_name,
                        match["rule_set_name"],
                        match["condition"],
                        clickable_path,
                        match["start"],
                        match["end"]
                    ])
                print(f"Processed {file_name} successfully.")'''
        
        # Define the path prefix for the subfolder structure
        path_prefix = app_settings.blob_path_prefix

        # Process each blob in the container
        for blob in list_blobs(app_settings.blob_service_client, app_settings.blob_container_name, path_prefix):
            blob_name = blob.name
            content = read_blob_content(app_settings.blob_service_client, app_settings.blob_container_name, blob_name)

            text_content = content.get('text_content', '')

            # Process the text content
            clickable_path = app_settings.original_path + blob_name
            extracted_info = process_text(text_content, rulesets)
            for match in extracted_info:
                csvwriter.writerow([
                    blob_name,
                    match["rule_set_name"],
                    match["condition"],
                    clickable_path,
                    match["start"],
                    match["end"]
                    ])
                print(f"Processed {blob_name} successfully.")

if __name__ == "__main__":
    main()