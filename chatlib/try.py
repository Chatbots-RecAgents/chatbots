from models.surprise_funcs import *

from datasets.python_splitters import python_random_split
from models.surprise_utils import (
    predict,
    compute_ranking_predictions,
)

# Top k items to recommend
TOP_K = 10
    # Specify the path to your CSV file
csv_file_path = "/Users/marianareyes/Desktop/ie_tower/chatbots-2/chatlib/datasets/ratings.csv"

    # Load data
data = load_data(csv_file_path)

    # Split data into train and test sets
train, test = python_random_split(data, 0.75)

    # Train the model
svd_model = train_model(train)

    # Make predictions
predictions = predict(svd_model, test, usercol="userID", itemcol="itemID")

    # Compute ranking predictions
all_predictions = compute_ranking_predictions(
    svd_model, train, usercol="userID", itemcol="itemID", remove_seen=True
)

    # Evaluate the model
evaluate_model(test, predictions, all_predictions, TOP_K)

    # Generate recommendations for a user
user_id_to_predict = 1  # Replace 1 with the actual user ID you want to predict for
top_10_recommendations = generate_recommendations(user_id_to_predict, svd_model, train)
print("Top 10 recommended items for user", user_id_to_predict)
print(top_10_recommendations)