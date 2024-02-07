# Description: This file contains the logic for processing text and extracting information based on rulesets.
from flashtext import KeywordProcessor
import json

def load_rulesets(ruleset_path):
    with open(ruleset_path, 'r') as file:
        rulesets = json.load(file)
    return rulesets

def process_text(text, rulesets):
    keyword_processor = KeywordProcessor()
    for ruleset in rulesets:
        for condition in ruleset["fulltext_conditions"]:
            keyword_processor.add_keyword(condition["condition"])
    
    found_keywords = keyword_processor.extract_keywords(text, span_info=True)
    # For simplicity, just return the found keywords for now
    return found_keywords

# Example usage within this file, you'll actually call process_text from main.py
if __name__ == "__main__":
    sample_text = "This is a test text containing some keywords like credit card and email address."
    ruleset_path = 'config/example_rulesets.json'  # Adjust path as necessary
    rulesets = load_rulesets(ruleset_path)
    extracted_info = process_text(sample_text, rulesets)
    print(extracted_info)
