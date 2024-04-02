from chatbot import AIChatbot
from unittest.mock import patch
from unittest.mock import patch, MagicMock
import unittest
import pandas as pd
import datetime


# Test AIChatbot initialization
def test_ai_chatbot_initialization():
    api_key = "test-api-key"
    chatbot = AIChatbot(openai_api_key=api_key)
    assert chatbot.openai_api_key == api_key
    assert chatbot.last_response == ""
    assert not any(chatbot.questions_asked.values())
    
# Test AIChatbot update_conversation method
def test_update_conversation():
    chatbot = AIChatbot(openai_api_key="test-api-key")
    user_message = "Hello, chatbot!"
    chatbot.update_conversation(user_message)
    assert "Human: Hello, chatbot!\nAI:" in chatbot.last_response

# Test AIChatbot handling OpenAI API errors in generate_response
@patch('openai.ChatCompletion.create')
def test_generate_response_api_error(mock_create):
    mock_create.side_effect = Exception("API error")
    chatbot = AIChatbot(openai_api_key="test-api-key")
    response, all_answered = chatbot.generate_response("Test message")
    assert response == "Sorry, I'm having trouble thinking of a response right now."
    assert not all_answered

# Test AIChatbot ask_next_question method
def test_ask_next_question():
    chatbot = AIChatbot(openai_api_key="test-api-key")
    chatbot.ask_next_question()
    assert "What's your name?" in chatbot.last_response
    assert chatbot.questions_asked['name']

# Test AIChatbot generate_response method
@patch('openai.ChatCompletion.create')
def test_generate_response(mock_create):
    mock_create.return_value = {
        'choices': [{'message': {'content': 'Mocked response'}}]
    }
    chatbot = AIChatbot(openai_api_key="test-api-key")
    response, all_answered = chatbot.generate_response("Test message")
    assert response == "Mocked response"
    assert not all_answered

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