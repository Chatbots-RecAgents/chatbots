from chatbot import AIChatbot
from unittest.mock import patch

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
