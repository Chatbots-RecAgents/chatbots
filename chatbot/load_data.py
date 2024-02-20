import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

def get_dataset(path):
    # Specify the path to your CSV file
    csv_file_path = path

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    return df

def encode_dataset(df):
    #One-hot encoding gender
    gender_encoder = OneHotEncoder()
    gender_encoded = gender_encoder.fit_transform(df[['gender']])
    gender_encoded_df = pd.DataFrame(gender_encoded.toarray(), columns=gender_encoder.categories_[0])


    #Label encoding major, nationality, language, and hobbies
    label_encoder = LabelEncoder()
    df['major_encoded'] = label_encoder.fit_transform(df['major'])
    df['nationality_encoded'] = label_encoder.fit_transform(df['nationality'])
    df['language_encoded'] = label_encoder.fit_transform(df['languages'])
    df['hobbies_encoded'] = label_encoder.fit_transform(df['hobbies'])

    # Concatenate the one-hot encoded gender DataFrame with the original DataFrame
    df = pd.concat([df, gender_encoded_df], axis=1)

    # Drop the original categorical columns
    df.drop(['gender', 'major', 'nationality', 'languages', 'hobbies'], axis=1, inplace=True)

    return df
