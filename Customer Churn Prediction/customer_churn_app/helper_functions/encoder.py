import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, OneHotEncoder
import joblib

# from customer_churn_app.create_feature_matrix import create_feature_matrix


def encode_features(data):
    # Binary features: categorical columns with only two categories (Yes/No, Male/Female, etc.)
    binary_features = ['gender', 'Partner', 'Dependents', 'PhoneService',
                       'MultipleLines_categorised"','OnlineSecurity_categorised', 'OnlineBackup_categorised',
                       'DeviceProtection_categorised', 'TechSupport_categorised', 'StreamingTV_categorised',
                       'StreamingMovies_categorised', 'PaperlessBilling']

    # Ordinal features: categorical variables with a natural order (e.g., contract length, tenure bins, pricing tiers)
    ordinal_features = ['Contract', 'tenure_bin', 'monthly_pricing_tiers']

    # Nominal features: categorical variables without an inherent order
    # (e.g., Internet type, payment method, billing flag) -
    nominal_features = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                        'DeviceProtection', 'TechSupport', 'StreamingTV',
                        'StreamingMovies', 'PaymentMethod', 'billing_flag']

    # Numeric features: automatically select all numeric columns
    # X_data = data
    # data = X_data[0]
    # feature_names = X_data[1]
    # numeric_features = data.select_dtypes(include='number')

    # Separate groups
    # Identify numeric features explicitly (not in ordinal, binary, or nominal groups)
    num_features = [col for col in data.columns
                    if col not in ordinal_features + binary_features + nominal_features]

    # Ordinal Encoding: For ordered categorical features (Contract, tenure_bin, monthly_pricing_tiers)
    ordinal_encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)

    # Fit-transform on training data
    x_data_ord = pd.DataFrame(
        ordinal_encoder.fit_transform(data[ordinal_features]),
        columns=ordinal_features,
        index=data.index
    )

    # Label Encoding: For binary features (Yes/No type variables)
    x_data_bin = data[binary_features].copy()

    for col in binary_features:
        le = LabelEncoder()

        # Fit + transform on training data
        x_data_bin[col] = le.fit_transform(data[col])

    # One-Hot Encoding: For unordered categorical variables
    ohe_data = OneHotEncoder(drop=None, handle_unknown="ignore",
                             sparse_output=False)  # full version keeps all categories
    # Full OHE (for tree models)
    X_data_nom = pd.DataFrame(
        ohe_data.fit_transform(data[nominal_features]),
        columns=ohe_data.get_feature_names_out(nominal_features),
        index=data.index
    )

    # Numeric features (kept as-is)
    x_matrix_num = data[num_features].copy()

    # Combine everything back into model-ready datasets
    X = pd.concat([x_matrix_num, x_data_ord, x_data_bin, X_data_nom], axis=1)

    del_features = ["DeviceProtection_categorised", "TechSupport_categorised", "InternetService_No",
                    "OnlineSecurity_No internet service", "OnlineBackup_No internet service",
                    "DeviceProtection_No internet service", "TechSupport_No internet service", "StreamingTV_No",
                    "StreamingTV_Yes", "StreamingMovies_No internet service", "high_engagement_loyalty",
                    "high_risk_contract", "recent_high_charge", "is_auto_pay", "is_electronic_check",
                    "entertainment_bundle", "paperless_autopay", "senior_loyal", "tenure_bin", "monthly_pricing_tiers",
                    "Partner", "Dependents", "PhoneService", "MultipleLines_categorised",
                    "OnlineSecurity_categorised", "OnlineBackup_categorised", "StreamingTV_categorised",
                    "StreamingMovies_categorised", "MultipleLines_No", "MultipleLines_No phone service",
                    "MultipleLines_Yes", "InternetService_DSL", "OnlineSecurity_Yes", "OnlineBackup_No",
                    "OnlineBackup_Yes", "DeviceProtection_No", "DeviceProtection_Yes", "TechSupport_Yes",
                    "StreamingTV_No internet service", "StreamingMovies_No", "StreamingMovies_Yes",
                    "PaymentMethod_Bank transfer (automatic)", "PaymentMethod_Credit card (automatic)",
                    "PaymentMethod_Mailed check", "billing_flag_billing_issue", "billing_flag_discount",
                    "billing_flag_ok"]

    X = X.drop(columns=del_features)

    joblib.dump(X.columns.tolist(), "customer_churn_app/feature_order.pkl")

    # Convert to a numpy array
    X = X.values

    return X
