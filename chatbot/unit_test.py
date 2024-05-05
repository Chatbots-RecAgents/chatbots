# unit_test.py

import pytest
import json
from unittest.mock import patch, MagicMock, mock_open
from conversation_manager import ConversationManager

# Test for the ConversationManager generate_response method
def test_generate_response():
    # Set up the ConversationManager and a mock for the OpenAI API
    cm = ConversationManager()
    cm.set_current_question("What is your diet?")

    # Mocking the OpenAI API response
    with patch('openai.ChatCompletion.create') as mock_openai:
        mock_openai.return_value = MagicMock(choices=[{'message': {'content': 'Thank you for sharing!'}}])
        
        # Simulating user input and testing the response generation
        response = cm.generate_response("I mostly eat plant-based foods.")
        mock_openai.assert_called_once()  # Verify that the API was called
        assert "Thank you for sharing!" in response  # Check that the response is as expected

# Test for the ConversationManager save_to_json method
def test_save_to_json():
    cm = ConversationManager()
    cm.current_entry = {"diet": "Vegan", "body_type": "Athletic"}  # Populate some data

    # Use mock_open to simulate file writing
    m = mock_open()
    with patch('builtins.open', m), patch('json.dump') as mock_json_dump:
        cm.save_to_json()
        m.assert_called_once_with('current_user_data.json', 'w')  # Check file is opened in write mode
        mock_json_dump.assert_called_once()  # Check json.dump was called

# Existing tests from your file
from chatbot.test import add_numbers  # Adjust import according to your actual structure
def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(-1, -1) == -2

# Fixture to simulate dataset
@pytest.fixture
def sample_data():
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=100, n_features=4, n_informative=2, n_redundant=2, random_state=42)
    data = [{"profile_data": "data" + str(i)} for i in range(X.shape[0])]
    params = {
        'boosting_type': 'gbdt',
        'objective': 'binary',
        'metric': 'binary_logloss',
    }
    return X, y, data, params

# Test for Firestore mock data
@pytest.fixture
def firestore_data():
    mock_firestore_data = [
        {'name': 'Alice', 'age': '30', 'gender': 'Female', 'major': 'Computer Science', 'year':2, 'nationality': 'American', 'languages': 'English', 'hobbies': 'Reading'},
        {'name': 'Bob', 'age': '22', 'gender': 'Male', 'major': 'Data Science', 'year': 3, 'nationality': 'Canadian', 'languages': 'French', 'hobbies': 'Writing'},
    ]
    docs = []
    for data in mock_firestore_data:
        doc = MagicMock()
        doc.to_dict = MagicMock(return_value=data)
        docs.append(doc)
    return docs

if __name__ == "__main__":
    pytest.main()
