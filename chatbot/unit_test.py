import unittest
from chatlib import surprise
from surprise import SVD, Dataset, Reader
import pandas as pd
from chatlib.datasets.python_splitters import python_random_split, predict, compute_ranking_predictions
from chatlib.evaluation.python_evaluation import rmse, mae, rsquared, exp_var

class TestSurpriseModel(unittest.TestCase):

    def setUp(self):
        # Load the data for testing
        self.data = pd.DataFrame({
            'userID': [1, 2, 1, 2, 1, 2, 1, 2],
            'itemID': [1, 2, 2, 3, 3, 1, 4, 5],
            'rating': [3.0, 2.0, 4.0, 5.0, 3.5, 2.5, 4.0, 5.0]
        })
        self.train, self.test = python_random_split(self.data, 0.75)

    def test_data_split(self):
        # Ensure the data is split approximately 75% for training
        self.assertAlmostEqual(len(self.train) / len(self.data), 0.75, delta=0.1)

    def test_model_training(self):
        # Test model training
        train_set = Dataset.load_from_df(self.train, Reader('ml-100k')).build_full_trainset()
        model = SVD()
        model.fit(train_set)  # This should not raise any exception

    def test_predictions(self):
        # Test the prediction function
        model = SVD()
        train_set = Dataset.load_from_df(self.train, Reader('ml-100k')).build_full_trainset()
        model.fit(train_set)
        predictions = predict(model, self.test, usercol='userID', itemcol='itemID')
        self.assertIsNotNone(predictions)
        self.assertFalse(predictions.empty)

    def test_evaluation_metrics(self):
        # Assuming predictions are precomputed and stored in `predictions`
        predictions = predict(model, self.test, usercol='userID', itemcol='itemID')
        self.assertAlmostEqual(rmse(self.test, predictions), expected_rmse, places=2)
        self.assertAlmostEqual(mae(self.test, predictions), expected_mae, places=2)

    # Add more tests for other functionalities like evaluation and recommendation

if __name__ == '__main__':
    unittest.main()
