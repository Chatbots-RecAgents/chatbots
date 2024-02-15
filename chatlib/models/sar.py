import logging

from utils.timer import Timer
#import the dataset with EDA
from utils.python_utils import binarize
from recommenders.models.sar import SAR #pip install?

def train_and_test_sar(train_data, test_data, top_k=10):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s')

    model = SAR(
        col_user="userID",
        col_item="itemID",
        col_rating="rating",
        col_timestamp="timestamp",
        similarity_type="jaccard",
        time_decay_coefficient=30,
        timedecay_formula=True,
        normalize=True
    )

    with Timer() as train_time:
        model.fit(train_data)

    print("Took {} seconds for training.".format(train_time.interval))

    with Timer() as test_time:
        top_k_recommendations = model.recommend_k_items(test_data, top_k=top_k, remove_seen=True)

    print("Took {} seconds for prediction.".format(test_time.interval))

    return top_k_recommendations