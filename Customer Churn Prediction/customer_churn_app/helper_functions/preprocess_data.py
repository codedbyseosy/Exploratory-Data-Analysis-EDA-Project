from create_feature_matrix import create_feature_matrix
from encoder import encode_features
import joblib
import pandas as pd


def preprocess_data(data):
    data = create_feature_matrix(data)
    data = encode_features(data)

    feature_names = joblib.load("customer_churn_app/feature_order.pkl")
    data = data.reindex(columns=feature_names, fill_value=0)

    return data


