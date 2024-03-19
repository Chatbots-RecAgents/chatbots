import lightgbm as lgb
import numpy as np
from sklearn.metrics import roc_auc_score, log_loss
from sklearn.metrics.pairwise import cosine_similarity
from chatlib.models.load_data import * #importing everything from the preprocessed data

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