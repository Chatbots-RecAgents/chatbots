import pandas as pd
from sklearn.preprocessing import LabelEncoder
from chatbot import data

df = pd.read_json('/Users/marianareyes/Documents/GitHub/chatbots/chatbot/data.json')

# Encode categorical variables
label_encoders = {}
categorical_columns = ["Gender", "Major", "Country of Origin", "Languages Spoken", "Hobbies"]
for column in categorical_columns:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column])

print(df.head())