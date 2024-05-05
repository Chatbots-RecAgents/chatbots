import pandas as pd
import os
import json
import openai
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class ConversationManager:
    def __init__(self):
        openai.api_key = "api_key_here"
        self.model = self.build_model()
        self.tokenizer = Tokenizer(num_words=10000)
        self.max_length = 20
        self.keys = ["age", "body_type", "diet", "drinks", "drugs", "education", 
                     "ethnicity", "height", "income", "job", "last_online", "location", "offspring", "orientation", "pets", 
                     "religion", "sex", "sign", "smokes", "speaks", "status"]
        self.current_entry = {key: None for key in self.keys}
        self.conversation_history = []
        self.current_question = None
        self.current_question_index = 0
        self.questions = [
            "How old are you?", "What is your body type?", "What is your diet?", "Do you drink alcohol?", 
            "Do you use drugs?", "What is your education level?", "What is your ethnicity?",
            "What is your height?", "What is your income?", "What is your job?", "When were you last online?", 
            "Where do you live?", "Do you have offspring?", "What is your sexual orientation?", "Do you have pets?",
            "What is your religion?", "What is your sex?", "What is your zodiac sign?",
            "Do you smoke?", "What languages do you speak?", "What is your marital status?"
        ]

    def build_model(self):
        model = Sequential([
            Embedding(input_dim=10000, output_dim=64, name='embedding_layer'), 
            GRU(128, return_sequences=True, name='gru_layer1'),
            GRU(64, name='gru_layer2'),
            Dense(64, activation='relu', name='dense_layer1'),
            Dense(1, activation='sigmoid', name='output_layer')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def analyze_input_with_gru(self, user_input):
        sequences = self.tokenizer.texts_to_sequences([user_input])
        padded = pad_sequences(sequences, maxlen=self.max_length)
        prediction = self.model.predict(padded)[0]
        sentiment = "positive" if prediction > 0.5 else "negative"
        return sentiment

    def set_current_question(self, question):
        self.current_question = question

    def update_conversation_history(self, user_input):
        question_key = self.keys[self.current_question_index]  # Use keys list to determine which attribute to update
        self.current_entry[question_key] = user_input
        self.current_question_index += 1
        if self.current_question_index >= len(self.questions):
            self.conversation_history.append(self.current_entry.copy())  # Append the complete set of answers
            self.save_to_json()  # Save the current entry to JSON after the conversation ends
            self.current_entry = {key: None for key in self.keys}  # Reset for new conversation
            print("Full conversation added to history:", self.conversation_history)

    def generate_response(self, user_input):
        if not self.current_question:
            return "No question set. Please set a question first."
        
        self.update_conversation_history(user_input)
        sentiment = self.analyze_input_with_gru(user_input)

        prompt = f"The user was asked about their '{self.current_question}' and answered '{user_input}'. Given this response indicates a '{sentiment}' sentiment, can you provide a fun and engaging comment or advice related to their answer?"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=150
        )
        generated_response = response.choices[0].message['content']
        return generated_response

    def save_conversation_to_csv(self):
            if self.conversation_history:
                df = pd.DataFrame(self.conversation_history, columns=self.keys)  # Specify columns to ensure correct order
                csv_file = 'conversation_history.csv'
                if not os.path.exists(csv_file):
                    df.to_csv(csv_file, mode='w', header=True, index=False)
                else:
                    df.to_csv(csv_file, mode='a', header=False, index=False)
                print("Conversation history saved to CSV.")

    def save_to_json(self):
        if self.current_entry:
            with open('current_user_data.json', 'w') as json_file:
                json.dump(self.current_entry, json_file, indent=4)
            print("Current user data saved to JSON.")

if __name__ == "__main__":
    cm = ConversationManager()
    print("Conversation Manager initialized.")
