# unit_test.py

import pytest
import json
import os
import json
from unittest.mock import patch, MagicMock, mock_open
from tensorflow.keras.layers import Embedding, GRU, Dense 

# Existing tests from your file
from chatbot.test import add_numbers  # Adjust import according to your actual structure
def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(-1, -1) == -2


import unittest
from .conversation_manager import ConversationManager  # Adjust the import path if necessary

class TestConversationManager(unittest.TestCase):
    def setUp(self):
        """Setup for test methods."""
        self.cm = ConversationManager()
    def test_build_model(self):
        model = self.cm.build_model()
        self.assertEqual(len(model.layers), 5)
        self.assertIsInstance(model.get_layer('embedding_layer'), Embedding)
        self.assertIsInstance(model.get_layer('gru_layer2'), GRU)
        self.assertIsInstance(model.get_layer('output_layer'), Dense)
    def test_analyze_input_with_gru(self):
        # Assuming that tokenizer and model are properly initialized and can handle the input "hello world"
        sentiment = self.cm.analyze_input_with_gru("hello world")
        self.assertIn(sentiment, ['positive', 'negative'])  # Ensuring it returns one of the expected sentiments
    def test_update_conversation_history(self):
        self.cm.set_current_question("What is your height?")
        self.cm.update_conversation_history("6 feet")
        self.assertEqual(self.cm.current_entry['height'], "6 feet")
        self.assertEqual(self.cm.current_question_index, 1)

    def test_save_to_json(self):
        self.cm.current_entry = {'height': '6 feet'}
        self.cm.save_to_json()
        with open('current_user_data.json', 'r') as file:
            data = json.load(file)
        self.assertEqual(data['height'], '6 feet')
        os.remove('current_user_data.json')  # Clean up after test
    from unittest.mock import patch

    def test_generate_response(self):
        with patch('openai.ChatCompletion.create') as mock_create:
            mock_create.return_value = {
                'choices': [{'message': {'content': 'Test response'}}]
            }
            response = self.cm.generate_response("Test input")
            self.assertIn('Test response', response)



if __name__ == "__main__":
    pytest.main()
