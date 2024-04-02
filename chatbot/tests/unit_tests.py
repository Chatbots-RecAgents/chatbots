from chatbotgpt import AIChatbot
from unittest.mock import patch
from unittest.mock import patch
import unittest
import pandas as pd
import datetime

class TestAIChatbot(unittest.TestCase):
    @patch('chatbot.AIChatbot')
    def test_ai_chatbot_initialization(self, MockChatbot):
        api_key = "test-api-key"
        chatbot = MockChatbot(openai_api_key=api_key)
        self.assertEqual(chatbot.openai_api_key, api_key)

    @patch('chatbot.AIChatbot')
    def test_update_conversation(self, MockChatbot):
        user_message = "Hello, chatbot!"
        chatbot = MockChatbot()
        chatbot.update_conversation(user_message)
        chatbot.update_conversation.assert_called_with(user_message)

    @patch('openai.ChatCompletion.create')
    def test_generate_response_api_error(self, mock_create):
        mock_create.side_effect = Exception("API error")
        chatbot = AIChatbot(openai_api_key="test-api-key")
        response, all_answered = chatbot.generate_response("Test message")
        self.assertEqual(response, "Sorry, I'm having trouble thinking of a response right now.")
        self.assertFalse(all_answered)

    @patch('openai.ChatCompletion.create')
    def test_generate_response(self, mock_create):
        mock_create.return_value = {
            'choices': [{'message': {'content': 'Mocked response'}}]
        }
        chatbot = AIChatbot(openai_api_key="test-api-key")
        response, all_answered = chatbot.generate_response("Test message")
        self.assertEqual(response, "Mocked response")
        self.assertFalse(all_answered)

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
    def test_save_to_csv(self, mock_to_csv):
        mock_responses = {
            'name': 'John Doe',
            'age': '30',
            'gender': 'Male',
            'nationality': 'USA',
            'major': 'Computer Science',
            'languages': 'English, Spanish',
            'hobbies': 'Reading, Coding'
        }
        
        save_to_csv(mock_responses)
        
        mock_to_csv.assert_called_once()

        args, kwargs = mock_to_csv.call_args
        self.assertEqual(kwargs['index'], False)
        self.assertEqual(args[0], "output.csv")

if __name__ == '__main__':
    unittest.main()