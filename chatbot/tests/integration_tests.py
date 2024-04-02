from chatbot import AIChatbot
from unittest.mock import patch

# Simulate a complete interaction cycle with the chatbot
@patch('openai.ChatCompletion.create')
def test_chatbot_interaction_cycle(mock_create):
    # Adjust mock side_effect to simulate a sequence of responses from the chatbot
    mock_create.side_effect = [
        {'choices': [{'message': {'content': 'Hi! What is your name?'}}]},  # Greeting response
        {'choices': [{'message': {'content': 'Nice to meet you, Alex. How old are you?'}}]}  # Follow-up question
    ]
    
    chatbot = AIChatbot(openai_api_key="test-api-key")
    
    # User starts the conversation with a greeting
    greeting_response, _ = chatbot.generate_response("Hello")
    
    # Ensure the chatbot uses the external API to generate a greeting response
    assert greeting_response == "Hi! What is your name?"
    
    # Simulate answering the chatbot's question with the user's name
    name_response, all_answered = chatbot.generate_response("My name is Alex.")
    
    # Verify the chatbot acknowledges the name correctly and asks a follow-up question
    assert name_response == "Nice to meet you, Alex. How old are you?"
    
    # Verify the chatbot has updated the user information based on the responses
    assert chatbot.user_info['name'] == "Alex"  
    
    # Verify the chatbot has updated the questions asked
    assert not all_answered  


@patch('openai.ChatCompletion.create')
def test_error_handling_and_recovery(mock_create):
    # First call to the API fails, but the second succeeds
    mock_create.side_effect = [Exception("API error"), 
                               {'choices': [{'message': {'content': 'Recovered response'}}]}]
    
    chatbot = AIChatbot(openai_api_key="test-api-key")
    
    # First request encounters an error
    response, _ = chatbot.generate_response("This should fail.")
    assert "Sorry, I'm having trouble thinking of a response right now." in response
    
    # The system recovers and processes the next request successfully
    recovered_response, _ = chatbot.generate_response("Try again.")
    assert "Recovered response" in recovered_response




    


