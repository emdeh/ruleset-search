# Description: This file contains the logic for processing text and extracting information based on rulesets.
from flashtext import KeywordProcessor
import json

def load_rulesets(ruleset_path):
    with open(ruleset_path, 'r') as file:
        rulesets = json.load(file)
    return rulesets

def process_text(text, rulesets):
    keyword_processor = KeywordProcessor()
    keyword_to_ruleset_map = {}

    # Adjusted mapping to support multiple rule sets for the same condition
    for ruleset in rulesets:
        rule_set_name = ruleset["rule_set_name"]
        for condition in ruleset["fulltext_conditions"]:
            keyword = condition["condition"]
            keyword_processor.add_keyword(keyword)
            if keyword not in keyword_to_ruleset_map:
                keyword_to_ruleset_map[keyword] = []
            keyword_to_ruleset_map[keyword].append((rule_set_name, keyword))

    found_keywords = keyword_processor.extract_keywords(text, span_info=True)
    results = []

    # Handling matches where a condition may belong to multiple rule sets
    for keyword, start, end in found_keywords:
        for rule_set_name, condition in keyword_to_ruleset_map[keyword]:
            results.append({
                "rule_set_name": rule_set_name,
                "condition": condition,
                "start": start,
                "end": end
            })

    return results

# Example usage within this file, you'll actually call process_text from main.py
if __name__ == "__main__":
    sample_text = "This is a test text containing some keywords like credit card and email address."
    ruleset_path = 'config/example_rulesets.json'  # Adjust path as necessary
    rulesets = load_rulesets(ruleset_path)
    extracted_info = process_text(sample_text, rulesets)
    print(extracted_info)
