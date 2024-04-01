import openai
import pandas as pd
from openai.error import OpenAIError

class AIChatbot:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key
        
        self.user_info = {
            "name": "",
            "age": "",
            "gender": "",
            "nationality": "",
            "major": "",
            "year": "",
            "languages": "",
            "hobbies": ""
        }
        
        self.questions_asked = {key: False for key in self.user_info.keys()}
        self.questions = [
            "What's your name?",
            "How old are you?",
            "What is your gender?",
            "Where are you from?",
            "What is your major?",
            "Which year are you in?",
            "Which languages do you speak?",
            "What are your hobbies?"
        ]
        self.last_response = ""
    
    def update_conversation(self, user_message):
        self.last_response += f"\nHuman: {user_message}\nAI:"
    
    def ask_next_question(self):
        for question, asked in self.questions_asked.items():
            if not asked:
                self.last_response += self.questions[len(self.user_info) - len(self.questions_asked) + list(self.questions_asked.keys()).index(question)]
                self.questions_asked[question] = True
                break

    def generate_response(self, user_message):
        self.update_conversation(user_message)
        
        if all(self.questions_asked.values()):
            return "All questions answered. Press 'Recommend' when ready.", True

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Using the correct API method for chat models
                messages=[
                    {"role": "system", "content": "You are interviewing the user to get some informations about him, make sure to only ask all the questions defined in {self.questions},but ask them sequentially and comment on each answer with a simple phrase then move on ."},
                    {"role": "user", "content": user_message},
                ]
            )
            
            generated_text = response.choices[0].message['content'].strip()
            self.last_response += generated_text
            self.ask_next_question()  # Ensure to ask the next question if needed
            return generated_text, False
        except Exception as e:  # Catching all exceptions for debugging
            print(f"Encountered an error: {e}")
            return "Sorry, I'm having trouble thinking of a response right now.", False
