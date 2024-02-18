import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for conversation flow
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0

# Questions and corresponding keys
questions = [
    ("What's your name?", "name"),
    ("How old are you?", "age"),
    ("What is your gender? (Feel free to specify as you wish)", "gender"),
    ("Where are you from?", "nationality"),
    ("What is your major at IE?", "major"),
    ("Which languages do you speak? (Separate by comma if more than one)", "languages"),
    ("What do you like to do in your free time?", "hobbies"),
]

# Function to move to the next question
def next_question():
    if st.session_state.current_question_index < len(questions) - 1:
        st.session_state.current_question_index += 1
    else:
        st.session_state.ready_to_finalize = True

# Display the current question
def display_current_question():
    if 'current_question_index' in st.session_state:
        # Unique key for each question based on its index to avoid DuplicateWidgetID error
        current_question, key = questions[st.session_state.current_question_index]
        unique_key = f"{key}_{st.session_state.current_question_index}"
        user_response = st.text_input(current_question, key=unique_key, on_change=next_question)
        
        if user_response:
            # Strip and save the response using the original key
            st.session_state.responses[key] = user_response.strip()

# Finalize conversation and save to CSV
def finalize_conversation():
    recommendation = "Based on your interests, you might enjoy playing tennis with Juan."
    name = st.session_state.responses.get('name', 'there')
    st.write(f"Hello {name}, {recommendation}")
    
    save_conversation(st.session_state.responses)
    # Reset for the next conversation
    st.session_state.responses.clear()
    st.session_state.current_question_index = 0

# Save conversation to a CSV file
def save_conversation(responses):
    new_row = {**responses, 'Recommendation': "Based on your interests, you might enjoy playing tennis with Juan.", 'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    new_row_df = pd.DataFrame([new_row])
    
    try:
        data = pd.read_csv('chatbot_data.csv')
    except FileNotFoundError:
        data = pd.DataFrame(columns=new_row.keys())
    
    updated_data = pd.concat([data, new_row_df], ignore_index=True)
    updated_data.to_csv('chatbot_data.csv', index=False)

st.title('HingE Chatbot')

# Manage the flow of the conversation
if 'ready_to_finalize' not in st.session_state or st.button("Start Over"):
    st.session_state.ready_to_finalize = False
    st.session_state.current_question_index = 0  # Reset to start from the first question

if st.session_state.ready_to_finalize:
    finalize_conversation()
    st.session_state.ready_to_finalize = False  # Reset for a new conversation
else:
    display_current_question()
