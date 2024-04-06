import streamlit as st
import pandas as pd
import os
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, get_app, App
from chatbot_comment import generate_comment

from chatlib.models.surprise_funcs import *
from chatlib.datasets.python_splitters import python_random_split

def initialize_firebase():
    try:
        # Try to retrieve the default app, assuming it has already been initialized.
        firebase_app = get_app()
    except ValueError:
        # If the default app has not been initialized, then initialize it.
        cred = credentials.Certificate("credentials.json")
        firebase_app = initialize_app(cred)
    
    # Initialize Firestore client
    db = firestore.client(app=firebase_app)
    
    return db

def load_data_from_firestore():
    """Load data from Firebase Firestore."""
    # Initialize Firestore client
    db = firestore.client()
    
    # Fetch data from the "ratings" collection
    ratings_ref = db.collection('ratings').get()
    
    # Extract required fields from documents
    ratings_data = []
    for doc in ratings_ref:
        doc_data = doc.to_dict()
        ratings_data.append({
            'userID': doc_data.get('userID'),
            'itemID': doc_data.get('itemID'),
            'rating': doc_data.get('rating')
        })

    # Fetch data from the "items" collection
    items_ref = db.collection('training_data').get()
    
    # Extract required fields from documents
    items_data = []
    for doc in items_ref:
        doc_data = doc.to_dict()
        items_data.append({
            'itemID': doc.get('itemID'),
            'name': doc_data.get('name'),
            'age': doc_data.get('age'),
            'nationality': doc_data.get('nationality'),
            'major': doc_data.get('major'),
            'hobbies': doc_data.get('hobbies'),
            'languages': doc_data.get('languages')
        })

    # Create DataFrames from the extracted data
    ratings_df = pd.DataFrame(ratings_data)
    items_df = pd.DataFrame(items_data)

    return ratings_df, items_df


# Initialize Firebase and get Firestore client
db = initialize_firebase()

# Function to get the next item ID
def get_next_item_id():
    docs = db.collection('training_data').stream()
    return sum(1 for _ in docs) + 1

# Function to update Firestore with the new responses, excluding the user_id
def update_responses(new_data):
    # Copy the data to avoid modifying the original dict
    data_to_save = new_data.copy()
    # Remove the user_id before saving
    if 'user' in data_to_save:
        del data_to_save['user']
    data_to_save['item_id'] = get_next_item_id()
    db.collection('training_data').add(data_to_save)

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

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
        st.session_state.responses = {}
        st.session_state.current_index = 0

    questions_and_fields = [
        ("What's your user_id?", "user"),
        ("What's your name?", "name"),
        ("How old are you?", "age"),
        ("What is your gender?", "gender"),
        ("Where are you from?", "nationality"),
        ("What is your major?", "major"),
        ("Which year are you in?", "year"),
        ("Which languages do you speak?", "languages"),
        ("What are your hobbies?", "hobbies"),
        ("Do you want your profile to be rated?", "consent")
    ]

    if 'user_id' not in st.session_state:
        user_input = st.text_input("Enter your User ID", key="user_input")
        if user_input and user_input.isdigit():
            st.session_state['user_id'] = int(user_input)
            st.session_state.current_index = 0  # Start the survey

    if 'user_id' in st.session_state:
        # If we have a user_id, proceed with the conversation
        if 0 <= st.session_state.current_index < len(questions_and_fields):
            question, field_key = questions_and_fields[st.session_state.current_index]
            bot_message = f"🤖: {question}"
            # Append bot's question to conversation history if it's not the last message
            if not st.session_state.conversation_history or st.session_state.conversation_history[-1] != bot_message:
                st.session_state.conversation_history.append(bot_message)

            # Display conversation history
            for message in st.session_state.conversation_history:
                if message.startswith("🤖"):
                    st.markdown(f"<div class='message-container'><div class='message bot-message'>{message}</div></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='message-container'><div class='message user-message'>{message}</div></div>", unsafe_allow_html=True)

            # User input field
            user_response = st.text_input("", key=f"response_{st.session_state.current_index}", placeholder="Type your answer here...")
            if user_response:
                # Append user response to conversation history and update session state
                user_message = f"You: {user_response}"
                st.session_state.conversation_history.append(user_message)
                if st.session_state.current_index > 0: # Save response if it's not the user_id
                    st.session_state.responses[field_key] = user_response

                # Generate and display the bot's comment
                comment = generate_comment(user_response)
                st.session_state.conversation_history.append(f"🤖: {comment}")

                # Increment the index to move to the next question
                st.session_state.current_index += 1

        # For the last question, handle consent directly within the loop
        if st.session_state.current_index == len(questions_and_fields) and st.session_state.responses.get("consent", "").lower() in ["yes", "y"]:
            update_responses(st.session_state.responses)
            st.success("Your responses have been saved. Thank you!")
            reset_session_state()
        elif st.session_state.current_index == len(questions_and_fields):
            st.success("You've chosen not to save your profile. Thank you for your time!")
            reset_session_state()

        #implent the model
        # Load data from Firestore
        data, items_df = load_data_from_firestore() #loading ratings and trainingdata collections
        st.write(items_df.head())

        train, test = python_random_split(data, 0.75)
        svd_model = train_model(train)

        # Use the user's inputted userID for predictions
        user_id_to_predict = st.session_state.user_id
        if user_id_to_predict:
            top_10_recommendations = generate_recommendations(user_id_to_predict, svd_model, train)
            #top_10_recommendations['itemID'] = top_10_recommendations['itemID'].astype(str)
            # Merge items_df with top_10_recommendations on 'itemID'
            merged_df = pd.merge(top_10_recommendations, items_df, on='itemID', how='left')
            st.write("Top 10 recommended items for user", user_id_to_predict)
            st.write(merged_df)

            # Construct the sentence for each row in the merged DataFrame
            sentences = []
            for index, row in merged_df.iterrows():
                sentence = f"{row['name']}, a {row['age']} year old from {row['nationality']}, with itemID: {row['itemID']} is a match for you! Studies {row['major']} and pursues the following hobbies: {row['hobbies']}. Languages spoken: {row['languages']}. Predicted rating: {row['prediction']} \n"
                sentences.append(sentence)

            # Join the sentences into a single string and display
            final_sentence = '\n'.join(sentences)
            st.write(final_sentence)
        else:
            st.warning("Please provide your user_id to get recommendations.")
    if st.button("Start Over"):
        reset_session_state()

def reset_session_state():
    """Helper function to reset the session state."""
    st.session_state.conversation_history = []
    st.session_state.responses = {}
    st.session_state.current_index = 0
    st.session_state.user_id = None

if __name__ == "__main__":
    main()