import streamlit as st
import pandas as pd
import os
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_chatbot import generate_comment

from chatlib.models.load_data_fb import *
from chatlib.models.lgbm_fb import *

# Check if Firebase app has already been initialized
if not firebase_admin._apps:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("credentials.json")  # Path to your service account key JSON file
    firebase_admin.initialize_app(cred)
else:
    # Firebase app already initialized
    print("Firebase app already initialized.")

# Initialize Firestore client
db = firestore.client()

# Define your questions and corresponding Firestore collection names
questions_and_fields = {
    "What's your name?": "name",
    "How old are you?": "age",
    "What is your gender?": "gender",
    "Where are you from?": "nationality",
    "What is your major?": "major",
    "Which year are you in?": "year",
    "Which languages do you speak?": "languages",
    "What are your hobbies?": "hobbies"
}

def update_responses(new_data):
    # Store the responses in Firestore
    db.collection('training_data').add(new_data)

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

    if st.session_state.current_index < len(questions_and_fields):
        question = list(questions_and_fields.keys())[st.session_state.current_index]
        field_name = questions_and_fields[question]

        # Display the bot's question if it's not already in the history
        if not st.session_state.conversation_history or st.session_state.conversation_history[-1]['content'] != question:
            st.session_state.conversation_history.append({'sender': 'bot', 'content': question})
            st.markdown(f"<div class='message-container'><div class='message bot-message'>🤖: {question}</div></div>", unsafe_allow_html=True)

        # User input field
        user_response = st.text_input("", key=f"question_{st.session_state.current_index}", placeholder="Type your answer here...")

        if user_response:
            # Store the response
            st.session_state.responses[field_name] = user_response

            # Add user response to the conversation history
            st.session_state.conversation_history.append({'sender': 'user', 'content': user_response})

            # Generate and display the bot's comment
            comment = generate_comment(user_response)
            st.session_state.conversation_history.append({'sender': 'bot', 'content': comment})

            # Increment the index to proceed to the next question and rerun the app
            st.session_state.current_index += 1
            st.rerun()

    elif st.session_state.current_index >= len(questions_and_fields):
        # Save the collected responses
        update_responses(st.session_state.responses)

        # Load data from Firestore
        data = load_data_from_firestore()

        # Preprocess data
        X, y = preprocess_data(data)

        params = {
            'boosting_type': 'gbdt',
            'objective': 'multiclass',
            'num_class': len(np.unique(y)),  # Number of unique names/classes
            'metric': 'multi_logloss',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.9
        }

        model = train_model(X, y, params)

        profile_index = len(X) - 1
        similar_profiles = find_similar_profiles(profile_index, data, X, model)

        # Thank the user and add the final message to the conversation history
        thank_you_message = "Thank you for participating!"
        st.session_state.conversation_history.append({'sender': 'bot', 'content': thank_you_message})
        st.markdown(f"<div class='message-container'><div class='message bot-message'>🤖: {thank_you_message}</div></div>", unsafe_allow_html=True)

        # Print similar profiles message
        similar_profiles_message = "Here are your top 5 matches:"
        st.session_state.conversation_history.append({'sender': 'bot', 'content': similar_profiles_message})
        st.markdown(f"<div class='message-container'><div class='message bot-message'>🤖: {similar_profiles_message}</div></div>", unsafe_allow_html=True)

        # Iterate over similar profiles and print profile descriptions
        for idx, profile in enumerate(similar_profiles, start=1):
            profile_description = f"{idx}. {profile['name']}: {profile['age']} year old {profile['gender'].lower()}, from {profile['nationality']}. "
            profile_description += f"Majoring in {profile['major']}. Languages: {profile['languages']}. Hobbies: {profile['hobbies']}."
            st.session_state.conversation_history.append({'sender': 'bot', 'content': profile_description})
            st.markdown(f"<div class='message-container'><div class='message bot-message'>🤖: {profile_description}</div></div>", unsafe_allow_html=True)
        
        # Reset the session state for a new conversation
        st.session_state.current_index = 0
        st.session_state.responses = {}
        st.session_state.conversation_history = []

if __name__ == '__main__':
    main()