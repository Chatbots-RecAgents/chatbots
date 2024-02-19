import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize or reset session state variables at the start
if 'init' not in st.session_state:
    st.session_state.responses = {}
    st.session_state.current_question_index = 0
    st.session_state.ready_to_finalize = False
    st.session_state.init = True

# Define questions and their corresponding keys
questions = [
    ("What's your name?", "name"),
    ("How old are you?", "age"),
    ("What is your gender?", "gender"),
    ("Where are you from?", "nationality"),
    ("What is your major at IE?", "major"),
    ("Which year are you in?", "year"),
    ("Which languages do you speak?", "languages"),
    ("What do you like to do in your free time?", "hobbies"),
]

def display_question():
    if st.session_state.current_question_index < len(questions):
        question, key = questions[st.session_state.current_question_index]
        response = st.text_input(question, key=key)
        
        # Automatically capture the response for the current question
        if response:
            st.session_state.responses[key] = response.strip()
        
        # Check if we are at the last question
        if st.session_state.current_question_index == len(questions) - 1:
            if st.button("Submit"):
                if response:  # Make sure the last response is not empty
                    finalize_conversation()
                else:
                    st.warning("Please answer the last question before submitting.")
        elif response:  # For any question except the last, move to the next question on response
            st.session_state.current_question_index += 1
            st.experimental_rerun()

def finalize_conversation():
    save_to_csv(st.session_state.responses)
    recommendation = "Based on your interests, you might enjoy playing tennis with Juan."
    st.write(f"Hello {st.session_state.responses.get('name', '')}, {recommendation}")
    st.success("Your responses have been saved!")

    # Remove the submit button and display the recommendation
    st.session_state.ready_to_finalize = True

def save_to_csv(responses):
    ordered_keys = ['name', 'age', 'gender', 'nationality', 'major', 'year', 'languages', 'hobbies', 'Recommendation', 'Timestamp']
    responses['Recommendation'] = "Based on your interests, you might enjoy playing tennis with Juan."
    responses['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ordered_responses = {key: responses.get(key, '') for key in ordered_keys}
    df = pd.DataFrame([ordered_responses], columns=ordered_keys)
    
    try:
        existing_data = pd.read_csv('chatbot_data.csv')
        updated_data = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        updated_data = df
    
    updated_data.to_csv('chatbot_data.csv', index=False, float_format='%.1f')

st.title('HingE Chatbot')

if not st.session_state.ready_to_finalize:
    display_question()
