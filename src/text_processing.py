# Description: This file contains the logic for processing text and extracting information based on rulesets.
from flashtext import KeywordProcessor
import json
import os
from dotenv import load_dotenv
import os
import nltk

def write_file_manifest(input_dir, output_dir, manifest_file='manifest.txt'):
    load_dotenv()
    input_dir = os.getenv('INPUT_DIR')
    output_dir = os.getenv('OUTPUT_DIR')
    manifest_file = os.path.join(output_dir, 'manifest.txt')

    with open(manifest_file, 'w') as file:
        for filename in os.listdir(input_dir):
            file.write(filename + '\n')

# Example usage within main.py
if __name__ == "__main__":
    write_file_manifest()


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

    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    sentence_starts = [text.find(sentence) for sentence in sentences]
    
    results = []

    # Handling matches where a condition may belong to multiple rule sets
    for keyword, start, end in found_keywords:

        # Find the sentence that contains the keyword
        # Find the sentence that contains the keyword
        sentence_index = next((i for i, s_start in enumerate(sentence_starts) if s_start > start), len(sentences)) - 1
        # Ensure the sentence_index is not less than 0 after adjustment
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

# Example usage within this file, you'll actually call process_text from main.py
if __name__ == "__main__":
    sample_text = "This is a test text containing some keywords like credit card and email address."
    ruleset_path = 'config/example_rulesets.json'  # Adjust path as necessary
    rulesets = load_rulesets(ruleset_path)
    extracted_info = process_text(sample_text, rulesets)
    print(extracted_info)
