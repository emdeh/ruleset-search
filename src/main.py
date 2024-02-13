# Description: This script demonstrates how to process text from Azure Blob Storage and write the results to a CSV file.
import sys
import os
from text_processing import write_file_manifest, process_text, load_rulesets
from azure_blob_utils import get_blob_service_client, list_blobs, read_blob_content
from azure.storage.blob import BlobServiceClient
import csv
import json # for testing

# Calculate the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root to the system path
sys.path.insert(0, project_root)

# import app_settings
from config import app_settings

def main():
    
    # Initialize the Azure Blob Service Client
    blob_service_client = get_blob_service_client(app_settings.blob_account_url, app_settings.blob_credential)
    print(f"Successfully connected to the Azure Blob Storage account: {app_settings.blob_account_url} with service client: {blob_service_client}")

    # Create manifest of input files
    write_file_manifest(blob_service_client, app_settings.blob_container_name, app_settings.blob_path_prefix, app_settings.output_dir, manifest_file='manifest.txt')

    # Load the rulesets from a JSON file
    rulesets = load_rulesets(app_settings.ruleset_path)   

    # Prepare the CSV file for output
    with open(app_settings.output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Name', 'Triggered Rule', 'Triggered Condition', 'Surrounding context (Extracts the the sentences immediately before and after where the condition was triggered)', 'Start', 'End', 'Path to File'])

        # Define the path prefix for the subfolder structure
        path_prefix = app_settings.blob_path_prefix
        print(f"Processing blobs in the container with path prefix: {path_prefix}")

        # Process each blob in the container
        print(f"Listing blobs in container: {app_settings.blob_container_name}")
        for blob in list_blobs(blob_service_client, app_settings.blob_container_name, path_prefix):
            print(f"Found blob: {blob.name}")
            blob_name = blob.name
            content = read_blob_content(blob_service_client, app_settings.blob_container_name, blob_name)
    
            if 'text_content' in content and content['text_content'].strip():
            # 'strip()' removes leading/trailing whitespace, making this check fail for empty or whitespace-only content
                text_content = content['text_content']
                print(f"Processing blob: {blob_name} with text content length: {len(text_content)}")
            
                # Process the text content
                clickable_path = app_settings.original_path + blob_name
                extracted_info = process_text(text_content, rulesets)
                for match in extracted_info:

                    # Compile the surrounding context for the current match in a list.
                    surrounding_context = [s for s in [match["prev_sentence"], match["sentence"], match["next_sentence"]] if s]

                    # Concatenate the surrounding context and strip any leading/trailing whitespace
                    surrounding_context_str = " ".join(surrounding_context).strip()
                    
                    # Write the match to the CSV file
                    csvwriter.writerow([
                        blob_name,
                        match["rule_set_name"],
                        match["condition"],
                        surrounding_context_str,  # Concatenated and stripped context
                        match["start"],
                        match["end"],
                        clickable_path
                    ])
                    print(f"Processed {blob_name} successfully.")
            else:
                # Handle blobs with empty or whitespace-only 'text_content'
                print(f"Skipping blob: {blob_name} due to empty 'text_content'")

if __name__ == "__main__":
    main()

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
                    # Compile the surrounding context for the current match in a list.
                    surrounding_context = [s for s in [match["prev_sentence"], match["sentence"], match["next_sentence"]] if s]

                    # Concatenate the surrounding context and strip any leading/trailing whitespace
                    surrounding_context_str = " ".join(surrounding_context).strip()

                    # Write the match to the CSV file
                    csvwriter.writerow([
                        file_name,
                        match["rule_set_name"],
                        match["condition"],
                        surrounding_context_str,  # Concatenated and stripped context
                        match["start"],
                        match["end"],
                        clickable_path
                    ])
                print(f"Processed {file_name} successfully.")
'''