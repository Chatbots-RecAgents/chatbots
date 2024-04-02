import streamlit as st
import os
from chatbotgpt import AIChatbot

# Fetch the OpenAI API key from the environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize your AIChatbot with the fetched API key
chatbot = AIChatbot(openai_api_key=openai_api_key)



st.title("AI Chatbot")

# Custom CSS to mimic WhatsApp chat style
st.markdown("""
<style>
    .message-container {
        display: flex;
        flex-direction: column;
    }
    .message {
        position: relative;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 8px;
        color: #fff;
    }
    .user-message {
        margin-left: auto;
        background-color: #056162;
    }
    .bot-message {
        margin-right: auto;
        background-color: #34B7F1;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Placeholder for displaying the conversation and handling chat history
chat_display = st.empty()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'all_answered' not in st.session_state:
    st.session_state['all_answered'] = False  # Initialize all_answered in session state

# Text input for the user message
user_input = st.text_input("Type your message here:", key="user_input", label_visibility="collapsed")

if user_input:
    st.session_state.chat_history.append(f"You: {user_input}")
    bot_response, st.session_state['all_answered'] = chatbot.generate_response(user_input)
    st.session_state.chat_history.append(f"AI: {bot_response}")

# Render the chat messages
chat_html = "<div class='message-container'>"
for message in st.session_state.chat_history:
    sender_class = "user-message" if message.startswith("You:") else "bot-message"
    chat_html += f"<div class='message {sender_class}'>{message}</div>"
chat_html += "</div>"
chat_display.markdown(chat_html, unsafe_allow_html=True)

# Show the 'Recommend' button if all questions have been answered
if st.session_state['all_answered']:
    if st.button('Recommend'):
        # Save the gathered information to a CSV file
        st.write("User information saved. Recommendations will be shown here.")