from chatbot.test import add_numbers
import numpy as np
import pytest
import lightgbm as lgb
from sklearn.datasets import make_classification
from chatlib.models.lgbm_fb import find_similar_profiles, train_model

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(-1, -1) == -2

# Fixture to simulate dataset
@pytest.fixture
def sample_data():
    X, y = make_classification(n_samples=100, n_features=4, n_informative=2, n_redundant=2, random_state=42)
    data = [{"profile_data": "data" + str(i)} for i in range(X.shape[0])]
    params = {
        'boosting_type': 'gbdt',
        'objective': 'binary',
        'metric': 'binary_logloss',
    }
    return X, y, data, params

def test_find_similar_profiles(sample_data):
    X, y, data, params = sample_data
    model = train_model(X, y, params)  # Train model to generate embeddings
    similar_profiles = find_similar_profiles(0, data, X, model)
    assert isinstance(similar_profiles, list)
    assert len(similar_profiles) == 5  # Expecting top 5 similar profiles
    # Further assertions can check for the structure or contents of similar_profiles

def test_train_model(sample_data):
    X, y, data, params = sample_data
    model = train_model(X, y, params)
    assert isinstance(model, lgb.basic.Booster)  # Ensure the model is a LightGBM Booster instance
    # Optionally, you can assert the model's performance on a held-out set or its structure




####################



import pytest
from unittest.mock import patch, MagicMock
from chatlib.models.load_data_fb import load_data_from_firestore, preprocess_data  # adjust the import path according to your project structure

# Mock data returned from Firestore
mock_firestore_data = [
    {'name': 'Alice', 'age': '30', 'gender': 'Female', 'major': 'Computer Science', 'nationality': 'American', 'languages': 'English', 'hobbies': 'Reading'},
    {'name': 'Bob', 'age': '22', 'gender': 'Male', 'major': 'Data Science', 'nationality': 'Canadian', 'languages': 'French', 'hobbies': 'Writing'},
    # Add more mock documents as needed for comprehensive testing
]

# Mock for Firestore document
class MockFirestoreDoc:
    def to_dict(self):
        pass

@pytest.fixture
def firestore_data():
    # Return a list of mock documents, converting each mock data entry to a mock Firestore document
    docs = []
    for data in mock_firestore_data:
        doc = MockFirestoreDoc()
        doc.to_dict = MagicMock(return_value=data)
        docs.append(doc)
    return docs

@patch('your_module.firestore.client')
def test_load_data_from_firestore(mock_firestore_client, firestore_data):
    # Setup mock
    mock_collection = mock_firestore_client().collection()
    mock_collection.get = MagicMock(return_value=firestore_data)

    # Call function
    data = load_data_from_firestore()

    # Assert
    assert len(data) == len(mock_firestore_data)
    for returned, expected in zip(data, mock_firestore_data):
        assert returned == expected

def test_preprocess_data():
    # Using mock_firestore_data as input
    X, y = preprocess_data(mock_firestore_data)

    # Perform various asserts
    # Assert the shape of X and y matches expectations
    # Assert specific processing results, like the correct encoding of categorical variables

    assert X.shape[0] == len(mock_firestore_data)  # Number of rows
    # Add more assertions as needed

