import streamlit as st
import pandas as pd

# Set the webpage title
st.set_page_config(page_title="HingE by IE")

# Create a header element
st.header("HingE by IE")

# List of questions to ask the user
questions = ["What's your name?",
             "What's your gender?",
             "How old are you?",
             "In which year are you?",
             "What's your degree?",
             "Where are you from?",
             "What languages can you speak?",
             "What are your hobbies?"]

# Store the conversation in the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Store the user responses in a dictionary
user_responses = {question: [] for question in questions}

# Store the current question index in the session state
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

# Display the current question
current_question = questions[st.session_state.question_index]
with st.chat_message("assistant"):
    st.markdown(current_question)

# Get user input
if current_question in ["What languages can you speak?", "What are your hobbies?"]:
    user_response = st.text_input("Your response here (comma-separated)", key=f"{current_question}_response")
    user_responses[current_question] = [item.strip() for item in user_response.split(',')]
else:
    user_response = st.text_input("Your response here", key=f"{current_question}_response")
    user_responses[current_question].append(user_response)

# Store the user's response in the session state
st.session_state.messages.append(
    {"role": "user", "content": user_response}
)

# Move to the next question if not the last one
if st.session_state.question_index < len(questions) - 1:
    st.session_state.question_index += 1
else:
    # Display the submit button at the last question
    if st.button("Submit"):
        # Create a DataFrame with user responses and save it to your dataset
        df = pd.DataFrame(user_responses.items(), columns=['Questions', 'Answers'])
        df.to_csv('generatedData.csv', index=False)  # Save DataFrame to CSV
        st.write("Conversation submitted!")
