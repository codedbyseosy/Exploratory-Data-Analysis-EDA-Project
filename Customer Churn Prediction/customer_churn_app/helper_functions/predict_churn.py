from helper_functions.preprocess_data import preprocess_data
import joblib
import os
import numpy as np


def predict_churn(data):
    """
    Predicts customer churn probability and classification using a trained model.

    Args:
        data: Input data for prediction (format depends on preprocess_data requirements).

    Returns:
        list: Contains [y_proba, churn_pred] where:
        - y_proba: Probability of churn for each sample.
        - churn_predL Binary classification (-=no churn, 1=churn) based on optimal threshold
    """

    # Step 1: Preprocess the input data into the format expectd by the model
    processed_data = preprocess_data(data)

    # DEBUG: Print processed data information for troubleshooting
    print(f"Processed data shape: {processed_data.shape}")
    print(f"Processed data columns: {list(processed_data.columns)}")

    # Step 2: Load the trained model and threshold
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    # Construct full paths to model files in the parent directory
    model_path = os.path.join(parent_dir, "final_cost_sensitive_voting_ensemble.pkl")
    thr_path = os.path.join(parent_dir, "best_threshold.pkl")

    # Load the pre-trained ensemble model
    model = joblib.load(model_path)

    # DEBUG: Check model's expected features for compatibility verification
    try:
        if hasattr(model, 'feature_names_in_'):
            print(f"Model expects features: {model.feature_names_in_}")
            print(f"Number of features model expects: {len(model.feature_names_in_)}")
    except:
        print("Could not get feature names from model")

    # Step 3: Generate predictions
    # Get probability estimates for both classes (typically [prob_class_0, prob_class_1])
    y_proba = model.predict_proba(processed_data)

    # Extract probabilities for the positive class (churn = 1)
    if isinstance(y_proba, np.ndarray):
        y_proba = y_proba[:, 1] # Extract probability of churn for each sample
    else:
        y_proba = np.array(y_proba)[:, 1] # Convert to numpy array if needed

    # Step 4: Load and apply optimal threshold
    best_thr = joblib.load("customer_churn_app/best_threshold.pkl")
    if not isinstance(best_thr, (float, int)):
        best_thr = float(best_thr[0])  # Safely extract scalar value if it's in an array

    # Apply threshold to convert probabilities to binary predictions
    churn_pred = (y_proba >= best_thr).astype(int)

    # Package results for return
    items = [y_proba, churn_pred]

    return items