import numpy as np
import lightgbm as lgb
import category_encoders as ce
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
#pip install lightgbm==3.3.5

#Defining lgbm parameters
MAX_LEAF = 128
MIN_DATA = 50
NUM_OF_TREES = 100
TREE_LEARNING_RATE = 0.1
EARLY_STOPPING_ROUNDS = 200
METRIC = "auc"
SIZE = "sample"

params = {
    "task": "train",
    "boosting_type": "gbdt",
    "num_class": 1,
    "objective": "binary",
    "metric": METRIC,
    "num_leaves": MAX_LEAF,
    "min_data": MIN_DATA,
    "boost_from_average": True,
    "num_threads": 20, 
    "feature_fraction": 0.8,
    "learning_rate": TREE_LEARNING_RATE,
}

label_encoder = LabelEncoder() 

def preprocess_df(path):
    df = pd.read_csv(path)
    df = df.dropna()

    # Dealing with the essay columns
    df['all_essays'] = df[['essay0', 'essay1', 'essay2', 'essay3', 'essay4', 'essay5', 'essay6', 'essay7', 'essay8', 'essay9']].apply(lambda x: ' '.join(x.dropna()), axis=1)
    df = df.drop(columns=['essay0', 'essay1', 'essay2', 'essay3', 'essay4', 'essay5', 'essay6', 'essay7', 'essay8', 'essay9'])
    df = df.drop(columns=['all_essays'])

    # Label encode categorical variables
    #label_encoder = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = label_encoder.fit_transform(df[col])

    return df

def ratings_prediction(given_profile, df):
    # Compute cosine similarity between the given profile and all other profiles
    given_profile_df = pd.DataFrame([given_profile])
    given_profile_encoded = given_profile_df.copy()
    for col in given_profile_encoded.select_dtypes(include=['object']).columns:
        given_profile_encoded[col] = label_encoder.fit_transform(given_profile_encoded[col])

    # Create a DataFrame with the given profile repeated for each row to match the dimensions of df
    given_profile_expanded = pd.concat([given_profile_encoded]*len(df), ignore_index=True)
    
    # Compute cosine similarity between the given profile and all other profiles
    cosine_sim_given = cosine_similarity(given_profile_expanded, df)
    df['rating'] = cosine_sim_given.mean(axis=0)

    # Normalize the ratings to be between 0 and 1
    df['rating'] = (df['rating'] - df['rating'].min()) / (df['rating'].max() - df['rating'].min())

    return df

def preprocess_lgbm(path, df):
    df_lgbm = pd.read_csv(path)

    # Dealing with the essay columns
    df_lgbm['all_essays'] = df_lgbm[['essay0', 'essay1', 'essay2', 'essay3', 'essay4', 'essay5', 'essay6', 'essay7', 'essay8', 'essay9']].apply(lambda x: ' '.join(x.dropna()), axis=1)
    df_lgbm = df_lgbm.drop(columns=['essay0', 'essay1', 'essay2', 'essay3', 'essay4', 'essay5', 'essay6', 'essay7', 'essay8', 'essay9'])
    df_lgbm = df_lgbm.drop(columns=['all_essays'])

    #Adding the rating column gathered through Feature Engineering
    merged_df = df_lgbm.merge(df[['rating']], how='left', left_index=True, right_index=True)
    
    return merged_df

def encode_csv(df, encoder, label_col, typ="fit"):
    if typ == "fit":
        df = encoder.fit_transform(df)
    else:
        df = encoder.transform(df)
    y = df[label_col].values
    del df[label_col]
    return df, y

def training_lgbm(merged_df):
    #defining the columns from our df
    nume_cols = ["age", "height", "income"]
    cate_cols = ["body_type", "diet", "drinks", "drugs", "education", "ethnicity", "job", "last_online",
                "location", "offspring", "orientation", "pets", "religion", "sex", "sign", "smokes",
                "speaks", "status"]
    label_col = "rating"

    # split data to 3 sets    
    length = len(merged_df)
    train_data = merged_df.loc[:0.8*length-1]
    valid_data = merged_df.loc[0.8*length:0.9*length-1]
    test_data = merged_df.loc[0.9*length:]

    #Encoding categorical variables with the oerdinal encoder
    ord_encoder = ce.ordinal.OrdinalEncoder(cols=cate_cols)
    train_x, train_y = encode_csv(train_data, ord_encoder, label_col)
    valid_x, valid_y = encode_csv(valid_data, ord_encoder, label_col, "transform")
    test_x, test_y = encode_csv(test_data, ord_encoder, label_col, "transform")

    lgb_train = lgb.Dataset(train_x, train_y.reshape(-1), params=params, categorical_feature=cate_cols)
    lgb_valid = lgb.Dataset(valid_x, valid_y.reshape(-1), reference=lgb_train, categorical_feature=cate_cols)
    lgb_test = lgb.Dataset(test_x, test_y.reshape(-1), reference=lgb_train, categorical_feature=cate_cols)
    lgb_model = lgb.train(params,
                        lgb_train,
                        num_boost_round=NUM_OF_TREES,
                        valid_sets=lgb_valid,
                        categorical_feature=cate_cols,
                        callbacks=[lgb.early_stopping(EARLY_STOPPING_ROUNDS)])
    
    return lgb_model, ord_encoder

def generate_lightGBM_recommendations(df: pd.DataFrame, lgb_model, ord_encoder, number_of_recommendations: int = 10) -> list:
    label_col = "rating"
    # Make predictions for all profiles
    full_dataset_x, _ = encode_csv(df, ord_encoder, label_col, "transform")
    all_preds = lgb_model.predict(full_dataset_x)

    # Get sorted predictions with the highest one first
    top_indices = np.argsort(all_preds)[::-1]

    # Get the top recommendations
    recommendations = []
    counter = 0
    for index in top_indices:
        if counter == number_of_recommendations:
            break
        if not np.isnan(df.iloc[index][label_col]):
            continue
        else:
            counter += 1
            recommendations.append((index, all_preds[index]))

    return recommendations