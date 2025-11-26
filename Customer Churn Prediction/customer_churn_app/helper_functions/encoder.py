import pandas as pd

def encode_features(data):
    """
    Encodes features for model prediction compatibility.

    This function prepares input data by ensuring all 20 expected features
    are present and properly encoded as numerical values for model inference.

    Args:
        data (pd.DataFrame): Input data containing raw features

    Returns:
        pd.DataFrame: Encoded features with exactly 20 columns in expected order
    """

    # Define the EXACT 20 features your model expects with proper encoding
    expected_features = [
        'SeniorCitizen', 'tenure', 'MonthlyCharges_log', 'TotalCharges_log',
        'average_charges_per_month', 'contract_loyalty', 'contract_progress',
        'ServiceCount', 'charge_tenure_ratio_log', 'security_bundle', 'is_long_contract',
        'family_flag', 'Contract', 'gender', 'PaperlessBilling',
        'InternetService_Fiber optic', 'OnlineSecurity_No',
        'TechSupport_No', 'PaymentMethod_Electronic check',
        'billing_flag_partial_month'
    ]

    # Create a new DataFrame with only numerical values
    X = pd.DataFrame(index=data.index)

    # Manual encoding for categorical variables
    for feature in expected_features:
        if feature in data.columns:
            # Handle categorical features that need manual encoding
            if feature == 'Contract':
                # Encode contract types: Month-to-month=0, One year=1, Two year=2
                contract_mapping = {'Month-to-month': 0, 'One year': 1, 'Two year': 2}
                X[feature] = data[feature].map(contract_mapping).fillna(0)

            elif feature == 'gender':
                # Encode gender: Female=0, Male=1
                gender_mapping = {'Female': 0, 'Male': 1}
                X[feature] = data[feature].map(gender_mapping).fillna(0)

            elif feature == 'PaperlessBilling':
                # Encode paperless billing: No=0, Yes=1
                billing_mapping = {'No': 0, 'Yes': 1}
                X[feature] = data[feature].map(billing_mapping).fillna(0)

            elif feature in ['InternetService_Fiber optic', 'OnlineSecurity_No',
                             'TechSupport_No', 'PaymentMethod_Electronic check',
                             'billing_flag_partial_month']:
                # These should already be one-hot encoded as 0/1
                # If they're strings, convert to numeric using mapping
                if data[feature].dtype == 'object':
                    mapping = {'No': 0, 'Yes': 1, 'Fiber optic': 1, 'Electronic check': 1, 'partial_month': 1}
                    X[feature] = data[feature].map(mapping).fillna(0)
                else:
                    X[feature] = data[feature]  # Already numeric, copy as-is

            else:
                # For numerical features, just copy them directly
                X[feature] = data[feature]

        else:
            # Create missing features with appropriate default values
            # This ensures the model receives all expected features even if input data is incomplete
            if feature in ['SeniorCitizen', 'tenure', 'contract_loyalty', 'ServiceCount',
                           'security_bundle', 'is_long_contract', 'family_flag',
                           'Contract', 'gender', 'PaperlessBilling']:
                X[feature] = 0  # integer defaults to 0
            elif feature in ['MonthlyCharges_log', 'TotalCharges_log', 'average_charges_per_month',
                             'contract_progress', 'charge_tenure_ratio_log']:
                X[feature] = 0.0  # float defaults to 0.0
            else:
                X[feature] = 0  # one-hot encoded defaults to 0

    # Final safety check: Ensure all data is numerical
    # Convert any remaining object types to numeric, coercing errors to NaN then filling with 0
    for col in X.columns:
        if X[col].dtype == 'object':
            print(f"Warning: Column {col} is still object type, converting to numeric")
            X[col] = pd.to_numeric(X[col], errors='coerce').fillna(0)

    # Ensure the features are in the exact order expected by the model
    # Model training was done with features in this specific order
    X = X[expected_features]

    # Debug output: Display final data types for verification
    print(f"✅ Encoded features. Final dtypes:")
    for col in X.columns:
        print(f"   {col}: {X[col].dtype}")

    return X


# Feature reference for different models:
"""Tree features: ['SeniorCitizen', 'tenure', 'MonthlyCharges_log', 'TotalCharges_log',
 'average_charges_per_month', 'contract_loyalty', 'contract_progress', 
 'ServiceCount', 'charge_tenure_ratio_log', 'security_bundle', 'is_long_contract',
  'family_flag', 'Contract', 'gender', 'PaperlessBilling',
   'InternetService_Fiber optic', 'OnlineSecurity_No', 
   'TechSupport_No', 'PaymentMethod_Electronic check',
    'billing_flag_partial_month']"""

"""Linear features: ['SeniorCitizen', 'charge_tenure_ratio_log', 'high_engagement_loyalty', 
'high_risk_contract', 'entertainment_bundle', 'Contract', 'tenure_bin', 
'Dependents', 'PhoneService', 'MultipleLines_categorised', 
'OnlineSecurity_categorised', 'TechSupport_categorised', 
'PaperlessBilling', 'InternetService_Fiber optic', 
'InternetService_No', 'PaymentMethod_Electronic check', 
'billing_flag_discount', 'billing_flag_ok'] """