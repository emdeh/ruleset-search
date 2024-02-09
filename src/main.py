# Description: This script demonstrates how to process text from Azure Blob Storage and write the results to a CSV file.
# from azure_blob_utils import get_blob_service_client, list_blobs_in_container, read_blob_content
from text_processing import process_text, load_rulesets
import csv
import os
from dotenv import load_dotenv
import json # for testing

def main():
    current_dir = os.path.dirname(__file__)  # Gets the directory where the script is located
    input_dir = os.path.join('data', 'input')
    output_csv_path = os.path.join('data', 'output', 'hits.csv')  # Correct path to the CSV
    input_dir = os.path.join('data', 'input')
    input_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]  # Correct path to the JSON

    # Load environment variables from .env file
    load_dotenv()

    # Load configuration settings, such as Azure connection strings and container name
    #connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    #container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
    ruleset_path = os.getenv('RULESET_PATH')

    # Initialize the Azure Blob Service Client
    #client = get_blob_service_client(connection_string)

    # Load the rulesets from a JSON file
    rulesets = load_rulesets(ruleset_path)   

    # Prepare the CSV file for output
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Name', 'Triggered Rule', 'Triggered Condition', 'Start', 'End'])

        # FOR TESTING #
        # Process the local JSON file
        for file_name in input_files:
            file_path = os.path.join(input_dir, file_name)
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
                        match["start"],
                        match["end"]
                    ])
                print(f"Processed {file_name} successfully.")
        
        # Process each blob in the container
        #for blob in list_blobs_in_container(client, container_name):
        #    blob_name = blob.name
        #    content = read_blob_content(client, container_name, blob_name)
            
        #    if content:
        #        extracted_info = process_text(content, rulesets)
        #        if extracted_info:
        #            for info in extracted_info:
        #                csvwriter.writerow([blob_name] + list(info))
        #            print(f"Processed {blob_name} successfully.")

if __name__ == "__main__":
    main()