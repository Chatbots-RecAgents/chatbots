import surprise
import pandas as pd
from utils.timer import Timer
from evaluation.python_evaluation import (
    rmse,
    mae,
    rsquared,
    exp_var,
    map_at_k,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)


def load_data(csv_file_path):
    """Load data from a CSV file into a pandas DataFrame."""
    return pd.read_csv(csv_file_path, usecols=['userID', 'itemID', 'rating'])


def train_model(train_data):
    """Train the SVD model."""
    svd = surprise.SVD(random_state=0, n_factors=200, n_epochs=30, verbose=True)
    train_set = surprise.Dataset.load_from_df(
        train_data, reader=surprise.Reader(rating_scale=(1, 5))
    ).build_full_trainset()
    with Timer() as train_time:
        svd.fit(train_set)
    print(f"Took {train_time.interval} seconds for training.")
    return svd


def evaluate_model(test_data, predictions, all_predictions, top_k):
    """Evaluate the model."""
    eval_rmse = rmse(test_data, predictions)
    eval_mae = mae(test_data, predictions)
    eval_rsquared = rsquared(test_data, predictions)
    eval_exp_var = exp_var(test_data, predictions)

    eval_map = map_at_k(test_data, all_predictions, col_prediction="prediction", k=top_k)
    eval_ndcg = ndcg_at_k(test_data, all_predictions, col_prediction="prediction", k=top_k)
    eval_precision = precision_at_k(
        test_data, all_predictions, col_prediction="prediction", k=top_k
    )
    eval_recall = recall_at_k(test_data, all_predictions, col_prediction="prediction", k=top_k)

    print(
        "RMSE:\t\t%f" % eval_rmse,
        "MAE:\t\t%f" % eval_mae,
        "rsquared:\t%f" % eval_rsquared,
        "exp var:\t%f" % eval_exp_var,
        sep="\n",
    )

    print("----")

    print(
        "MAP:\t\t%f" % eval_map,
        "NDCG:\t\t%f" % eval_ndcg,
        "Precision@K:\t%f" % eval_precision,
        "Recall@K:\t%f" % eval_recall,
        sep="\n",
    )


def generate_recommendations(user_id, svd, train_data):
    """Generate recommendations for a user."""
    items_seen_by_user = train_data[train_data['userID'] == user_id]['itemID'].tolist()
    unseen_items = [item for item in train_data['itemID'].unique() if item not in items_seen_by_user]
    user_predictions = [(item, svd.predict(user_id, item).est) for item in unseen_items]
    sorted_predictions = sorted(user_predictions, key=lambda x: x[1], reverse=True)
    top_10_results = sorted_predictions[:10]
    top_10_df = pd.DataFrame(top_10_results, columns=['itemID', 'prediction'])
    return top_10_df