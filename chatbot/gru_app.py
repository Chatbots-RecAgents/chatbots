import streamlit as st
from conversation_manager import ConversationManager
from lgbm_funcs import *
import os
import json

def apply_custom_css():
    css = """
    <style>
        .stTextInput>label, .stButton>label { display: none; }
        .chat-bubble { padding: 10px; border-radius: 25px; margin-bottom: 10px; width: fit-content; max-width: 60%; }
        .user-bubble { background-color: #f0f0f0; align-self: flex-end; margin-right: 10px; color: #333; }
        .bot-bubble { background-color: #0099ff; color: white; align-self: flex-start; margin-left: 10px; }
        .question-bubble { background-color: #dddddd; color: black; border-radius: 15px; padding: 10px; margin: 10px 0; width: auto; }
        .chat-container { display: flex; flex-direction: column; margin: 5px; overflow-y: auto; padding-bottom: 50px; }
        body { background-color: whitesmoke; }
        .stTextInput { width: 90%; margin-left: auto; margin-right: auto; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    st.title('Chatbot Interface')
    apply_custom_css()
    if 'conv_manager' not in st.session_state:
        st.session_state.conv_manager = ConversationManager()

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    if 'current_question_index' not in st.session_state or st.session_state.current_question_index >= len(st.session_state.conv_manager.questions):
        st.session_state.current_question_index = 0  # Reset if out of range

    question = st.session_state.conv_manager.questions[st.session_state.current_question_index]
    st.session_state.conv_manager.set_current_question(question)
    st.markdown(f"<div class='question-bubble'>{question}</div>", unsafe_allow_html=True)
    user_input = st.text_input("Type your answer here...", key=f'user_input_{st.session_state.current_question_index}')

    if st.button("Submit", key=f'submit_{st.session_state.current_question_index}'):
        if user_input:
            response = st.session_state.conv_manager.generate_response(user_input)
            st.session_state.conversation.append({'user': user_input, 'bot': response})
            st.session_state.current_question_index += 1
            if st.session_state.current_question_index < len(st.session_state.conv_manager.questions):
                st.experimental_rerun()
            else:
                st.session_state.conv_manager.save_conversation_to_csv()
                st.success("All questions answered. Data saved.")
                st.session_state.current_question_index = 0  

    for chat in st.session_state.conversation:
            st.markdown(f"<div class='chat-bubble user-bubble'>{chat['user']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-bubble bot-bubble'>{chat['bot']}</div>", unsafe_allow_html=True)
        
    if st.session_state.current_question_index == 0 and st.session_state.conversation:
        # Recommendation part
        path = "/Users/sanabarakat/Desktop/year 3/semester 2/chatbots/chatbots/chatlib/models/profiles.csv"

        df_preprocessed = preprocess_df(path)

        json_path = 'current_user_data.json'
        if os.path.exists(json_path):
            with open(json_path, 'r') as json_file:
                given_profile = json.load(json_file)

            #Computing the ratings
            rated_df = ratings_prediction(given_profile, df_preprocessed)

            #Preprocessing dataset for lgbm
            preprocessed_lgbm = preprocess_lgbm(path, rated_df)

            #training lgbm
            lgb_model, ord_encoder = training_lgbm(preprocessed_lgbm)

            # Getting recommendations
            recommendations = generate_lightGBM_recommendations(preprocessed_lgbm, lgb_model, ord_encoder, 10)
            recommendations_data = []
            for index, (profile_index, prediction) in enumerate(recommendations, start=1):
                profile_info = preprocessed_lgbm.loc[profile_index]  # Get profile information from the preprocessed dataframe
                profile_message = f"Recommendation {index}: \n"
                profile_message += f"Profile index: {profile_index}: A {profile_info['age']} year old {profile_info['ethnicity']} "
                profile_message += f"{ 'male' if profile_info['sex'] == 'm' else 'female' } who is {profile_info['status']}, "
                profile_message += f"located in {profile_info['location']}."
                rounded_prediction = round(prediction, 4)  # Round the prediction to 4 decimal places
                recommendations_data.append((profile_message, f"You would rate this profile as: {rounded_prediction}"))            
            st.write("Top 10 recommendations:")
            for rec in recommendations_data:
                st.write(rec[0])
                st.write(rec[1])

if __name__ == "__main__":
    main()
