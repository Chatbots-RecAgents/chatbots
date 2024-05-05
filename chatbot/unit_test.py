import unittest
import pandas as pd
from chatlib.datasets.python_splitters import python_random_split

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

if __name__ == '__main__':
    unittest.main()
