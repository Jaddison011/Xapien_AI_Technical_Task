import unittest

from Xapien_AI_Technical_Task.main import *


class MockLLM:
    def __init__(self, mock_response: str):
        self.mock_response = mock_response

    def complete(self, prompt: str) -> str:
        return self.mock_response


class EntityExtractorTests(unittest.TestCase):
    def test_valid_formatting(self):
        mock_client = MockLLM('{"persons": ["John Doe", "Alice", "Bob"], "organisations": ["Acme Corp", "Giga Tech"]}')
        entity_extractor = EntityExtractor(mock_client)
        parsed_response = entity_extractor.extract_entities("Test Document")
        expected_response = {'persons': ['John Doe', 'Alice', 'Bob'], 'organisations': ['Acme Corp', 'Giga Tech']}
        self.assertDictEqual(expected_response, parsed_response, "Failed parsing valid LLM response")

    def test_cleaning_non_ascii_keys(self):
        mock_client = MockLLM('{"perso‰¿ns¿": ["John Doe", "Alice", "Bob"], "¿org‰anisat¿ions": ["Acme Corp", "Giga Tech"]}')
        entity_extractor = EntityExtractor(mock_client)
        parsed_response = entity_extractor.extract_entities("Test Document")
        expected_response = {'persons': ['John Doe', 'Alice', 'Bob'], 'organisations': ['Acme Corp', 'Giga Tech']}
        self.assertDictEqual(expected_response, parsed_response, "Failed parsing LLM response containing keys with non-ascii values")

    def test_cleaning_unquoted_keys(self):
        mock_client = MockLLM('{"persons": ["John Doe", "Alice", "Bob"], organisations: ["Acme Corp", "Giga Tech"]}')
        entity_extractor = EntityExtractor(mock_client)
        parsed_response = entity_extractor.extract_entities("Test Document")
        expected_response = {'persons': ['John Doe', 'Alice', 'Bob'], 'organisations': ['Acme Corp', 'Giga Tech']}
        self.assertDictEqual(expected_response, parsed_response, "Failed parsing LLM response containing non-quoted keys")

    def test_key_casing(self):
        mock_client = MockLLM('{"PeRsOns": ["John Doe", "Alice", "Bob"], oRGANIsatioNS: ["Acme Corp", "Giga Tech"]}')
        entity_extractor = EntityExtractor(mock_client)
        parsed_response = entity_extractor.extract_entities("Test Document")
        expected_response = {'persons': ['John Doe', 'Alice', 'Bob'], 'organisations': ['Acme Corp', 'Giga Tech']}
        self.assertDictEqual(expected_response, parsed_response, "Failed parsing LLM response containing uppercase keys")


if __name__ == '__main__':
    unittest.main()

