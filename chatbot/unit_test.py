from chatbot.test import add_numbers
import numpy as np
import pytest
from sklearn.datasets import make_classification

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



####################

# test1

import pytest
from unittest.mock import patch, MagicMock

# test
# Mock data returned from Firestore
mock_firestore_data = [
    {'name': 'Alice', 'age': '30', 'gender': 'Female', 'major': 'Computer Science', 'year':2, 'nationality': 'American', 'languages': 'English', 'hobbies': 'Reading'},
    {'name': 'Bob', 'age': '22', 'gender': 'Male', 'major': 'Data Science', 'year': 3, 'nationality': 'Canadian', 'languages': 'French', 'hobbies': 'Writing'},
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

