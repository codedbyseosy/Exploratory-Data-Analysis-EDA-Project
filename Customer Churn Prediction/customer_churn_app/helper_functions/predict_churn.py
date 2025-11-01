from helper_functions.preprocess_data import preprocess_data
import joblib
import os
import numpy as np


def predict_churn(data):
    processed_data = preprocess_data(data)

    # DEBUG: Check what features we have
    print(f"Processed data shape: {processed_data.shape}")
    print(f"Processed data columns: {list(processed_data.columns)}")

    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    # Construct paths to model files in the parent directory
    model_path = os.path.join(parent_dir, "final_cost_sensitive_voting_ensemble.pkl")
    thr_path = os.path.join(parent_dir, "best_threshold.pkl")

    model = joblib.load(model_path)

    # DEBUG: Check what features the model expects
    try:
        if hasattr(model, 'feature_names_in_'):
            print(f"Model expects features: {model.feature_names_in_}")
            print(f"Number of features model expects: {len(model.feature_names_in_)}")
    except:
        print("Could not get feature names from model")

    y_proba = model.predict_proba(processed_data)
    if isinstance(y_proba, np.ndarray):
        y_proba = y_proba[:, 1]
    else:
        y_proba = np.array(y_proba)[:, 1]

    # Step 4: Load best threshold
    best_thr = joblib.load("customer_churn_app/best_threshold.pkl")
    if not isinstance(best_thr, (float, int)):
        best_thr = float(best_thr[0])  # safely extract scalar

    churn_pred = (y_proba >= best_thr).astype(int)

    items = [y_proba, churn_pred]

    return items