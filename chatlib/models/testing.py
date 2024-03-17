from lgbm import *

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