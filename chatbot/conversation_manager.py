import pandas as pd
import numpy as np
import os
import openai
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class ConversationManager:
    def __init__(self):
        openai.api_key = "API-KEY" 
        self.model = self.build_model()
        self.conversation_history = []  # Store full conversation history
        self.current_question = None
        self.current_question_index = 0
        self.questions = [
            "What is your body type?", "What is your diet?", "Do you drink alcohol?", 
            "Do you use drugs?", "What is your education level?", "What is your ethnicity?",
            "What is your height?", "What is your income?", "What is your job?", 
            "Do you have offspring?", "What is your sexual orientation?", "Do you have pets?",
            "What is your religion?", "What is your sex?", "What is your zodiac sign?",
            "Do you smoke?", "What languages do you speak?", "What is your marital status?"
        ]
        self.tokenizer = Tokenizer(num_words=10000)  # Assuming a vocab size of 10000 for tokenizer
        self.max_length = 20  

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
        # Tokenize and pad the input text
        sequences = self.tokenizer.texts_to_sequences([user_input])
        padded = pad_sequences(sequences, maxlen=self.max_length)

        # Predict the sentiment or category from the GRU model
        prediction = self.model.predict(padded)[0]

        # Interpret the prediction as needed, for example, as a sentiment
        sentiment = "positive" if prediction > 0.5 else "negative"
        return sentiment

    def set_current_question(self, question):
        self.current_question = question

    def update_conversation_history(self, user_input, bot_response):
        # Ensure conversation history is a list of dictionaries with question-answer pairs
        if len(self.conversation_history) < len(self.questions):
            current_entry = {
                "body_type": None,
                "diet": None,
                "drinks": None,
                "drugs": None,
                "education": None,
                "ethnicity": None,
                "height": None,
                "income": None,
                "job": None,
                "offspring": None,
                "orientation": None,
                "pets": None,
                "religion": None,
                "sex": None,
                "sign": None,
                "smokes": None,
                "speaks": None,
                "status": None
            }
            # This assumes that self.current_question_index is maintained accurately
            question_key = self.questions[self.current_question_index].lower().replace("what is your ", "").replace("do you ", "").replace("?", "").replace(" ", "_")
            current_entry[question_key] = user_input
            self.conversation_history.append(current_entry)
            

    def generate_response(self, user_input):
        if not self.current_question:
            return "No question set. Please set a question first."

        self.update_conversation_history('user', user_input)
        sentiment = self.analyze_input_with_gru(user_input)

        fun_fact = "Remember, balance is key in everything!"
        prompt = f"The user was asked about their '{self.current_question}' and answered '{user_input}'. Given this response indicates a '{sentiment}' sentiment, can you provide a fun and engaging comment or advice related to their answer? For example, {fun_fact}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=150
        )
        generated_response = response.choices[0].message['content']
        self.update_conversation_history('assistant', generated_response)
        return generated_response


    def save_conversation_to_csv(self):
        if self.conversation_history:
            df = pd.DataFrame(self.conversation_history)
            df = df[['body_type', 'diet', 'drinks', 'drugs', 'education', 'ethnicity', 'height',
                    'income', 'job', 'offspring', 'orientation', 'pets', 'religion', 'sex',
                    'sign', 'smokes', 'speaks', 'status']]  
            csv_file = 'conversation_history.csv'
            if not os.path.exists(csv_file):
                df.to_csv(csv_file, mode='w', header=True, index=False)
            else:
                df.to_csv(csv_file, mode='a', header=False, index=False) 