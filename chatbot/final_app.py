import streamlit as st
import pandas as pd
import os
from final_comment import generate_comment

# Path for the CSV file to store responses
CSV_FILE_PATH = 'user_responses.csv'

# Define your questions and corresponding CSV column names
questions_and_columns = [
    ("What's your name?", "name"),
    ("How old are you?", "age"),
    ("What is your gender?", "gender"),
    ("Where are you from?", "nationality"),
    ("What is your major?", "major"),
    ("Which year are you in?", "year"),
    ("Which languages do you speak?", "languages"),
    ("What are your hobbies?", "hobbies")
]

def load_responses():
    if os.path.exists(CSV_FILE_PATH):
        return pd.read_csv(CSV_FILE_PATH)
    else:
        return pd.DataFrame(columns=[col for _, col in questions_and_columns])

def update_responses(df, new_data):
    new_df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    new_df.to_csv(CSV_FILE_PATH, index=False)

def main():
    st.title("Chatbot Survey")

    # Custom CSS for WhatsApp-like conversation styling
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
                border-bottom-right-radius: 0;
            }
            .bot-message {
                margin-right: auto;
                background-color: #34B7F1;
                border-bottom-left-radius: 0;
            }
            .stTextInput>div>div>input {
                border-radius: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Load existing responses
    responses_df = load_responses()

    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
        st.session_state.responses = {}
        st.session_state.conversation_history = []

    # Display conversation history
    for message in st.session_state.conversation_history:
        if message['sender'] == 'bot':
            st.markdown(f"<div class='message-container'><div class='message bot-message'>🤖: {message['content']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='message-container'><div class='message user-message'>{message['content']}</div></div>", unsafe_allow_html=True)

    if st.session_state.current_index < len(questions_and_columns):
        question, column_name = questions_and_columns[st.session_state.current_index]

        # Display the bot's question if it's not already in the history
        if not st.session_state.conversation_history or st.session_state.conversation_history[-1]['content'] != question:
            st.session_state.conversation_history.append({'sender': 'bot', 'content': question})
            st.markdown(f"<div class='message-container'><div class='message bot-message'>🤖: {question}</div></div>", unsafe_allow_html=True)

        # User input field
        user_response = st.text_input("", key=f"question_{st.session_state.current_index}", placeholder="Type your answer here...")

        if user_response:
            # Store the response
            st.session_state.responses[column_name] = user_response

            # Add user response to the conversation history
            st.session_state.conversation_history.append({'sender': 'user', 'content': user_response})

            # Generate and display the bot's comment
            comment = generate_comment(user_response)
            st.session_state.conversation_history.append({'sender': 'bot', 'content': comment})

            # Increment the index to proceed to the next question and rerun the app
            st.session_state.current_index += 1
            st.rerun()

    elif st.session_state.current_index >= len(questions_and_columns):
        # Save the collected responses
        update_responses(responses_df, st.session_state.responses)

        # Thank the user and add the final message to the conversation history
        thank_you_message = "Thank you for participating!"
        st.session_state.conversation_history.append({'sender': 'bot', 'content': thank_you_message})
        st.markdown(f"<div class='message-container'><div class='message bot-message'>🤖: {thank_you_message}</div></div>", unsafe_allow_html=True)

        # Reset the session state for a new conversation
        st.session_state.current_index = 0
        st.session_state.responses = {}
        st.session_state.conversation_history = []

if __name__ == '__main__':
    main()