import sys
import logging
import numpy as np
import pandas as pd
from sklearn.preprocessing import minmax_scale

from recommenders.utils.timer import Timer
from recommenders.datasets import movielens
from recommenders.utils.python_utils import binarize
from recommenders.datasets.python_splitters import python_stratified_split
from recommenders.models.sar import SAR
from recommenders.evaluation.python_evaluation import (
    map,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
    rmse,
    mae,
    logloss,
    rsquared,
    exp_var
)
from recommenders.utils.notebook_utils import store_metadata

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