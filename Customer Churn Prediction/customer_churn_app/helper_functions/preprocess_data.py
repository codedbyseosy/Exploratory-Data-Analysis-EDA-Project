from helper_functions.create_feature_matrix import create_feature_matrix
from helper_functions.encoder import encode_features
import joblib
import pandas as pd


def preprocess_data(data):
    data = create_feature_matrix(data)
    data = encode_features(data)

    # FORCE everything to be numeric and exactly 20 features
    final_data = data.copy()

    # Ensure we have exactly 20 columns
    if len(final_data.columns) > 20:
        final_data = final_data.iloc[:, :20]
    elif len(final_data.columns) < 20:
        for i in range(len(final_data.columns), 20):
            final_data[f'Column_{i}'] = 0

    # Rename to Column_0 to Column_19
    final_data.columns = [f'Column_{i}' for i in range(20)]

    # Convert all data to float
    final_data = final_data.astype(float)

    print(f"✅ Preprocessing complete: {final_data.shape}, all dtypes: {final_data.dtypes.unique()}")

    return final_data






# def preprocess_data(data):
#     print("Raw data dtypes:")
#     print(data.dtypes)
#     print("Raw data sample:")
#     print(data.head())
#
#     data = create_feature_matrix(data)
#     print("After feature engineering:")
#     print(data.dtypes)
#     print(data.head())
#
#     data = encode_features(data)
#     print("After encoding:")
#     print(data.shape)
#     print(data.columns)
#
#     feature_names = joblib.load("customer_churn_app/feature_order.pkl")
#     data = data.reindex(columns=feature_names, fill_value=0)
#
#     return data