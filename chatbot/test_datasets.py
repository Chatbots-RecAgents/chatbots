import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime

def save_to_csv(responses):
    ordered_keys = ['name', 'age', 'gender', 'nationality', 'major', 'languages', 'hobbies', 'Recommendation', 'Timestamp']
    responses['Recommendation'] = "Based on your interests, you might enjoy playing tennis with Juan."
    responses['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ordered_responses = {key: responses.get(key, '') for key in ordered_keys}
    df = pd.DataFrame([ordered_responses])
    df.to_csv("output.csv", index=False)

class TestSaveToCSV(unittest.TestCase):
    @patch('pandas.DataFrame.to_csv')
    @patch('pandas.DataFrame')
    def test_save_to_csv(self, mock_df, mock_to_csv):
        mock_df_instance = MagicMock()
        mock_df.return_value = mock_df_instance

        mock_responses = {
            'name': 'John Doe',
            'age': '30',
            'gender': 'Male',
            'nationality': 'USA',
            'major': 'Computer Science',
            'languages': 'English, Spanish',
            'hobbies': 'Reading, Coding'
        }
        
        expected_ordered_keys = ['name', 'age', 'gender', 'nationality', 'major', 'languages', 'hobbies', 'Recommendation', 'Timestamp']
        
        save_to_csv(mock_responses)
        
        mock_df.assert_called_once()
        df_call_args, df_call_kwargs = mock_df.call_args
        constructed_df_data = df_call_args[0]
        
        constructed_columns = list(constructed_df_data[0].keys())
        self.assertListEqual(constructed_columns, expected_ordered_keys)

if __name__ == '__main__':
    unittest.main()