import lightgbm as lgb
import numpy as np
from sklearn.metrics import roc_auc_score, log_loss
from sklearn.metrics.pairwise import cosine_similarity
from load_data import * #importing everything from the preprocessed data

def train_model(X, y, params):
    lgb_dataset = lgb.Dataset(X, label=y)
    # Train the model
    model = lgb.train(params, lgb_dataset)
    return model

def evaluate_model(model, X, y):
    # Make predictions
    test_preds = model.predict(X)
    # Evaluate model performance
    auc = roc_auc_score(np.asarray(y), test_preds, multi_class='ovo')  
    logloss = log_loss(np.asarray(y), test_preds, eps=1e-12)
    return {"auc": auc, "logloss": logloss}

def find_similar_profiles(profile_index, df, X, model, top_n=5):
    profile = X[profile_index].reshape(1, -1)
    similarities = cosine_similarity(profile, X)
    similar_indices = np.argsort(similarities)[0][-top_n-1:-1][::-1]
    similar_profiles = df.iloc[similar_indices]
    return similar_profiles

#testing
csv_file_path = "/Users/marianareyes/Documents/GitHub/chatbots/chatbot/data.csv"
df = load_data(csv_file_path)
X, y = preprocess_data(df)
params = {
    'boosting_type': 'gbdt',
    'objective': 'multiclass',
    'num_class': len(df['name_encoded'].unique()),  # Number of unique names/classes
    'metric': 'multi_logloss',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9
}
model = train_model(X, y, params)
evaluation_result = evaluate_model(model, X, y)
print(evaluation_result)

similar_profiles = find_similar_profiles(0, df, X, model)
print(similar_profiles)