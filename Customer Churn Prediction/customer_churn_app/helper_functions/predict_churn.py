from preprocess_data import preprocess_data
import joblib

def predict_churn(data):
    processed_data = preprocess_data(data)

    model = joblib.load("customer_churn_app/final_cost_sensitive_voting_ensemble.pkl")

    y_proba = model.predict_proba(processed_data)[:,1]

    churn_pred = (y_proba >= best_thr).astype(int)

    items = [y_proba, churn_pred]

    return items