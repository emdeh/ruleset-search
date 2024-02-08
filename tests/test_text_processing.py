import unittest
from src.text_processing import process_text  # Ensure this import path matches your project structure

class TestTextProcessing(unittest.TestCase):
    def test_keyword_detection(self):
        sample_text = "This is a test text containing some keywords like The Committee noted that changes in legislation in Newcastle, and InternationalBankingAccountNumber."
        rulesets = [
            {
                "rule_set_name": "Test phrase finding",
                "fulltext_conditions": [
                    {"condition": "The Committee noted that changes in legislation in Newcastle"}
                ]
            },
            {
                "rule_set_name": "Overseas Locations",
                "fulltext_conditions": [
                    {"condition": "Newcastle"},
                    {"condition": "InternationalBankingAccountNumber"}
                ]
            }
        ]

        # Expected outcome should match the format of process_text's return
        # For simplicity, let's assume it returns just the matched keywords as strings, but adjust this based on your actual function's return format
        expected_keywords = ["The Committee noted that changes in legislation in", "Newcastle", "InternationalBankingAccountNumber"]

        # Process the text
        found_keywords = process_text(sample_text, rulesets)

        # Flatten the found_keywords if it contains more than just the strings (e.g., span information) and compare
        found_keywords_flat = [item[0] for item in found_keywords]  # Adjust based on actual structure
        self.assertEqual(found_keywords_flat, expected_keywords)

if __name__ == '__main__':
    unittest.main()
