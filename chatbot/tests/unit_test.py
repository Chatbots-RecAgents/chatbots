import pandas as pd
from chatlib.models.surprise_funcs import load_data
from chatlib.models.surprise_utils import predict
from chatlib.datasets.pandas_df_utils import user_item_pairs, load_data, has_columns, has_same_base_dtype
from chatlib.utils.constants import DEFAULT_USER_COL, DEFAULT_ITEM_COL

# Mocking an algo for testing
class MockAlgo:
    def predict(self, user, item):
        return 0.5
    
mock_algo = MockAlgo()


# Surprise_funcs - load_data
def test_load_data(self):
    # Assuming a test CSV exists with known data
    test_csv = 'chatbot/test_data.csv'
    df = load_data(test_csv)
    self.assertIsInstance(df, pd.DataFrame)
    self.assertTrue(set(['userID', 'itemID', 'rating']).issubset(df.columns))


# 
def test_predict(self):
    # Assuming you have a mock algo and a small DataFrame of user/item pairs
    test_data = pd.DataFrame({
        'userID': [1, 2],
        'itemID': [10, 20]
    })
    # You might need to mock algo.predict or use a real, simple algo
    predictions_df = predict(mock_algo, test_data, usercol='userID', itemcol='itemID')
    self.assertIsInstance(predictions_df, pd.DataFrame)
    self.assertTrue(set(['userID', 'itemID', 'prediction']).issubset(predictions_df.columns))

# 
def test_user_item_pairs(self):
    user_df = pd.DataFrame({DEFAULT_USER_COL: [1, 2]})
    item_df = pd.DataFrame({DEFAULT_ITEM_COL: [3, 4]})
    expected = pd.DataFrame({
        DEFAULT_USER_COL: [1, 1, 2, 2],
        DEFAULT_ITEM_COL: [3, 4, 3, 4]
    })
    result = user_item_pairs(user_df, item_df, shuffle=False)
    pd.testing.assert_frame_equal(result, expected)


def test_has_columns(self):
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    self.assertTrue(has_columns(df, ['col1', 'col2']))
    self.assertFalse(has_columns(df, ['col1', 'col3']))

def test_has_same_base_dtype(self):
    df1 = pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})
    df2 = pd.DataFrame({'col1': [3.0, 4.0], 'col2': ['C', 'D']})
    self.assertTrue(has_same_base_dtype(df1, df1))
    self.assertFalse(has_same_base_dtype(df1, df2, columns=['col1']))
