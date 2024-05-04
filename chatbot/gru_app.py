import streamlit as st
from conversation_manager import ConversationManager

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

if __name__ == "__main__":
    main()