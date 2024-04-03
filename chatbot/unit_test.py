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
