from firebase_admin import firestore
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

def load_data_from_firestore():
    # Initialize Firestore client
    db = firestore.client()
    
    # Fetch data from the "training_data" collection
    training_data_ref = db.collection('training_data')
    docs = training_data_ref.get()
    
    # Extract data from documents
    data = []
    for doc in docs:
        data.append(doc.to_dict())
    
    return data

def preprocess_data(data):
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Filter out rows where 'age' column cannot be converted to integer
    df = df[pd.to_numeric(df['age'], errors='coerce').notna()]

    # One-hot encoding gender
    gender_encoder = OneHotEncoder()
    gender_encoded = gender_encoder.fit_transform(df[['gender']])
    gender_encoded_df = pd.DataFrame(gender_encoded.toarray(), columns=gender_encoder.categories_[0])

    # Label encoding major, nationality, language, and hobbies
    label_encoder = LabelEncoder()
    df['major_encoded'] = label_encoder.fit_transform(df['major'])
    df['nationality_encoded'] = label_encoder.fit_transform(df['nationality'])
    df['language_encoded'] = label_encoder.fit_transform(df['languages'])
    df['hobbies_encoded'] = label_encoder.fit_transform(df['hobbies'])

    # Encode the 'name' column
    name_encoder = LabelEncoder()
    df['name_encoded'] = name_encoder.fit_transform(df['name'])

    # Combine encoded features with numerical features
    encoded_cols = ['major_encoded', 'nationality_encoded', 'language_encoded', 'hobbies_encoded']
    numerical_cols = ['age', 'year']
    X = np.concatenate([gender_encoded_df.values, df[encoded_cols].values, df[numerical_cols]], axis=1)
    y = df['name_encoded']
    return X, y
