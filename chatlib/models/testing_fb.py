import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np

from load_data_fb import *
from lgbm_fb import *

# Check if Firebase app has already been initialized
if not firebase_admin._apps:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("/Users/marianareyes/Desktop/ie_tower/chatbots/chatbot/credentials.json")  # Path to your service account key JSON file
    firebase_admin.initialize_app(cred)
else:
    # Firebase app already initialized
    print("Firebase app already initialized.")

# Initialize Firestore client
db = firestore.client()

# Load data from Firestore
data = load_data_from_firestore()

# Preprocess data
X, y = preprocess_data(data)

params = {
    'boosting_type': 'gbdt',
    'objective': 'multiclass',
    'num_class': len(np.unique(y)),  # Number of unique names/classes
    'metric': 'multi_logloss',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9
}

model = train_model(X, y, params)

# Assuming profile_index is 0 for example
profile_index = len(X) - 1
similar_profiles = find_similar_profiles(profile_index, data, X, model)
print(similar_profiles)