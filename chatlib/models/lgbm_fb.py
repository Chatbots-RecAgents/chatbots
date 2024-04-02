import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import lightgbm as lgb

def find_similar_profiles(profile_index, data, X, model, top_n=5):
    profile = X[profile_index].reshape(1, -1)
    similarities = cosine_similarity(profile, X)
    similar_indices = np.argsort(similarities)[0][-top_n-1:-1][::-1]
    similar_profiles = [data[i] for i in similar_indices]
    return similar_profiles

def train_model(X, y, params):
    lgb_dataset = lgb.Dataset(X, label=y)
    model = lgb.train(params, lgb_dataset)
    return model