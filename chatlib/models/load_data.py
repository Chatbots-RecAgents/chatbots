import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

def load_data(csv_file_path):
    # Load data from CSV file
    df = pd.read_csv(csv_file_path)
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    return df

def preprocess_data(df):
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