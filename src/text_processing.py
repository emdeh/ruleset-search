# Description: This file contains the logic for processing text and extracting information based on rulesets.
from flashtext import KeywordProcessor
import json
import os
from dotenv import load_dotenv
import nltk
from azure.storage.blob import BlobServiceClient

def write_file_manifest(blob_service_client, blob_container_name, blob_path_prefix, output_dir='', manifest_file='manifest.txt'):
    load_dotenv()
    
    # Load output_dir from .env if not passed as an argument, and define the manifest file path.
    if not output_dir:
        output_dir = os.getenv('OUTPUT_DIR')
    manifest_file_path = os.path.join(output_dir, manifest_file)

    # Open the manifest file for writing, creating it if it doesn't exist/truncating it if it does.
    with open(manifest_file_path, 'w') as file:
        container_client = blob_service_client.get_container_client(blob_container_name)
        
        # List blobs with the specified prefix.
        blobs = container_client.list_blobs(name_starts_with=blob_path_prefix)
        for blob in blobs:
            # Remove the prefix directly to ensure no character is mistakenly dropped.
            partial_name = blob.name.replace(blob_path_prefix, '', 1)

            # Extract just the file name, assuming it's the portion after the last '/'.
            file_name = partial_name.split('/')[-1]
            
            # Optional: Remove a specific suffix if needed, e.g., '.output.json'.
            file_name = file_name.replace('.output.json', '')
            
            # Write the file name to the manifest file.
            file.write(file_name + '\n')

    print(f"Manifest file written to: {manifest_file_path}")

# Example usage within main.py
if __name__ == "__main__":
    write_file_manifest()

# Function to load rulesets from a JSON file.
def load_rulesets(ruleset_path):
    with open(ruleset_path, 'r') as file:
        rulesets = json.load(file)
    return rulesets

# Function to process text and extract information based on rulesets.
def process_text(text, rulesets):
    keyword_processor = KeywordProcessor()
    keyword_to_ruleset_map = {}

    # Support for duplicate conditions across rule sets.
    for ruleset in rulesets:
        rule_set_name = ruleset["rule_set_name"]
        for condition in ruleset["fulltext_conditions"]:
            keyword = condition["condition"]
            keyword_processor.add_keyword(keyword)
            if keyword not in keyword_to_ruleset_map:
                keyword_to_ruleset_map[keyword] = []
            keyword_to_ruleset_map[keyword].append((rule_set_name, keyword))

    found_keywords = keyword_processor.extract_keywords(text, span_info=True)

    # Tokenize the text into sentences.
    sentences = nltk.sent_tokenize(text)
    sentence_starts = [text.find(sentence) for sentence in sentences]
    
    results = []

    # Handle matches where a condition may belong to multiple rule sets.
    for keyword, start, end in found_keywords:

        # Find the sentence that contains the keyword
        sentence_index = next((i for i, s_start in enumerate(sentence_starts) if s_start > start), len(sentences)) - 1

        # Ensure sentence_index is not less than 0 after adjustment.
        sentence_index = max(sentence_index, 0)
        sentence = sentences[sentence_index]
        prev_sentence = sentences[sentence_index - 1] if sentence_index - 1 >= 0 else ""
        next_sentence = sentences[sentence_index + 1] if sentence_index + 1 < len(sentences) else ""
    
        for rule_set_name, condition in keyword_to_ruleset_map[keyword]:
            results.append({
                "rule_set_name": rule_set_name,
                "condition": condition,
                "start": start,
                "end": end,
                "sentence": sentence,
                "prev_sentence": prev_sentence,
                "next_sentence": next_sentence
            })

    return results

# Example usage within this file, but actual usage in main.py.
if __name__ == "__main__":
    sample_text = "This is a test text containing some keywords like credit card and email address."
    ruleset_path = 'config/example_rulesets.json'  # Adjust path as necessary
    rulesets = load_rulesets(ruleset_path)
    extracted_info = process_text(sample_text, rulesets)
    print(extracted_info)
