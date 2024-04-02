import openai
import streamlit as st
import os
from chatbotgpt import AIChatbot
# Fetch the OpenAI API key from the environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize your AIChatbot with the fetched API key
chatbot = AIChatbot(openai_api_key=openai_api_key)

def generate_comment(previous_answer):
    """
    Generates a comment using the OpenAI Chat Completion API.
    """
    try:
        # Construct the chat message
        chat_message = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Based on the user's response '{previous_answer}', generate a thoughtful comment without asking follow-up questions you just react"},
                {"role": "user", "content": previous_answer}
            ]
        }
        
        # Make the request to the chat completions endpoint
        response = openai.ChatCompletion.create(**chat_message)
        comment = response['choices'][0]['message']['content']
        return comment.strip()
    except Exception as e:
        print(f"Error generating comment: {e}")
        return "That's quite interesting! Please continue."