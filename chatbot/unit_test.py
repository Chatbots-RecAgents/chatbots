import unittest
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
import os
import json
from chatlib.datasets.python_splitters import python_random_split

# Mock the openai import to avoid errors during testing environments where it is not available
class openai:
    class ChatCompletion:
        @staticmethod
        def create(model, messages, max_tokens):
            return type('obj', (object,), {'choices': [{'message': {'content': 'Test response'}}]})

# Import the ConversationManager class
from .conversation_manager import ConversationManager  # Make sure to replace 'your_module' with the actual module name if used

class TestConversationManager(unittest.TestCase):
    def setUp(self):
        self.cm = ConversationManager()
        self.cm.api_key = "test_key"  # Mocking the api key for security reasons

    def test_build_model(self):
        """Test that the model is built correctly and compilation succeeds."""
        model = self.cm.build_model()
        self.assertIsInstance(model, Sequential)

    def test_analyze_input_with_gru(self):
        """Test the analysis of input through the GRU model."""
        self.cm.tokenizer.fit_on_texts(["test input"])
        sentiment = self.cm.analyze_input_with_gru("test input")
        self.assertIn(sentiment, ["positive", "negative"])

    def test_update_conversation_history(self):
        """Test updating the conversation history with new input."""
        self.cm.set_current_question(self.cm.questions[0])  # Set the first question
        self.cm.update_conversation_history("Yes")
        self.assertEqual(self.cm.current_entry[self.cm.keys[0]], "Yes")

    def test_save_to_json(self):
        """Test saving the current entry to JSON."""
        self.cm.current_entry = {"test": "data"}
        json_file = 'current_user_data.json'
        if os.path.exists(json_file):
            os.remove(json_file)
        self.cm.save_to_json()
        with open(json_file, 'r') as file:
            data = json.load(file)
            self.assertEqual(data, {"test": "data"})

    def test_save_conversation_to_csv(self):
        """Test saving the conversation history to CSV."""
        csv_file = 'conversation_history.csv'
        if os.path.exists(csv_file):
            os.remove(csv_file)
        
        # Update the conversation history with the correct keys
        self.cm.conversation_history = [{key: 'test data' for key in self.cm.keys}]
        self.cm.save_conversation_to_csv()
        
        df = pd.read_csv(csv_file)
        
        # Creating an expected dictionary with all keys set to 'test data'
        expected_data = {key: 'test data' for key in self.cm.keys}
        self.assertDictEqual(df.to_dict(orient='records')[0], expected_data)


# Adding existing tests for comparison with your data and model testing
class TestSurpriseModel(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'userID': [1, 2, 1, 2, 1, 2, 1, 2],
            'itemID': [1, 2, 2, 3, 3, 1, 4, 5],
            'rating': [3.0, 2.0, 4.0, 5.0, 3.5, 2.5, 4.0, 5.0]
        })
        self.train, self.test = python_random_split(self.data, 0.75)

    def test_data_split(self):
        self.assertAlmostEqual(len(self.train) / len(self.data), 0.75, delta=0.1)

if __name__ == '__main__':
    unittest.main()
