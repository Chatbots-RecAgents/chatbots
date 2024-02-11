import streamlit as st
import json
import os

# Set the webpage title
st.set_page_config(page_title="HingE by IE")

# Create a header element
st.header("HingE by IE")

# Load data from data.json
with open("data.json", "r") as data_file:
    data = json.load(data_file)

# List of questions to ask the user
questions = [
    "What's your name?",
    "What's your gender?",
    "How old are you?",
    "In which year are you?",
    "What's your degree?",
    "Where are you from?",
    "What languages can you speak?",
    "What are your hobbies?"
]

# Store the conversation in the session state
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

# Display the current question
if st.session_state.question_index < len(questions):
    current_question = questions[st.session_state.question_index]
    with st.expander("Question"):
        st.write(current_question)

    # Get user input
    user_response = st.text_input(f"Your response for '{current_question}'", key=f"{current_question}_response")

    # Store the user's response and save it immediately
    if st.button("Submit"):
        # Update the data dictionary with the user response
        data[st.session_state.question_index][current_question] = user_response.strip()
        
        # Save the updated data back to data.json
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Move to the next question
        st.session_state.question_index += 1

        # If all questions are answered, display a success message
        if st.session_state.question_index >= len(questions):
            st.success("Conversation submitted!")
else:
    st.write("All questions have been answered. Conversation completed.")
