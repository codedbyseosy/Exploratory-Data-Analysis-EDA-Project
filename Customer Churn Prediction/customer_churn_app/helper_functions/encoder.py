import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, OneHotEncoder
import joblib, os


def encode_features(data):
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
                # Encode contract types
                contract_mapping = {'Month-to-month': 0, 'One year': 1, 'Two year': 2}
                X[feature] = data[feature].map(contract_mapping).fillna(0)

            elif feature == 'gender':
                # Encode gender
                gender_mapping = {'Female': 0, 'Male': 1}
                X[feature] = data[feature].map(gender_mapping).fillna(0)

            elif feature == 'PaperlessBilling':
                # Encode paperless billing
                billing_mapping = {'No': 0, 'Yes': 1}
                X[feature] = data[feature].map(billing_mapping).fillna(0)

            elif feature in ['InternetService_Fiber optic', 'OnlineSecurity_No',
                             'TechSupport_No', 'PaymentMethod_Electronic check',
                             'billing_flag_partial_month']:
                # These should already be one-hot encoded as 0/1
                # If they're strings, convert to numeric
                if data[feature].dtype == 'object':
                    mapping = {'No': 0, 'Yes': 1, 'Fiber optic': 1, 'Electronic check': 1, 'partial_month': 1}
                    X[feature] = data[feature].map(mapping).fillna(0)
                else:
                    X[feature] = data[feature]

            else:
                # For numerical features, just copy them
                X[feature] = data[feature]

        else:
            # Create missing features with default values
            if feature in ['SeniorCitizen', 'tenure', 'contract_loyalty', 'ServiceCount',
                           'security_bundle', 'is_long_contract', 'family_flag',
                           'Contract', 'gender', 'PaperlessBilling']:
                X[feature] = 0  # integer defaults to 0
            elif feature in ['MonthlyCharges_log', 'TotalCharges_log', 'average_charges_per_month',
                             'contract_progress', 'charge_tenure_ratio_log']:
                X[feature] = 0.0  # float defaults to 0.0
            else:
                X[feature] = 0  # one-hot encoded defaults to 0

    # Ensure all data is numerical
    for col in X.columns:
        if X[col].dtype == 'object':
            print(f"Warning: Column {col} is still object type, converting to numeric")
            X[col] = pd.to_numeric(X[col], errors='coerce').fillna(0)

    # Ensure the features are in the exact order expected by the model
    X = X[expected_features]

    print(f"✅ Encoded features. Final dtypes:")
    for col in X.columns:
        print(f"   {col}: {X[col].dtype}")

    return X

# def encode_features(data):
#     binary_features = ['gender', 'Partner', 'Dependents', 'PhoneService',
#                        'MultipleLines_categorised', 'OnlineSecurity_categorised', 'OnlineBackup_categorised',
#                        'DeviceProtection_categorised', 'TechSupport_categorised', 'StreamingTV_categorised',
#                        'StreamingMovies_categorised', 'PaperlessBilling']
#
#     ordinal_features = ['Contract', 'tenure_bin', 'monthly_pricing_tiers']
#     nominal_features = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
#                         'DeviceProtection', 'TechSupport', 'StreamingTV',
#                         'StreamingMovies', 'PaymentMethod', 'billing_flag']
#
#     # CRITICAL FIX: Define num_features OUTSIDE the if/else block
#     num_features = [col for col in data.columns if col not in ordinal_features + binary_features + nominal_features]
#
#     encoders_dir = "../encoders"
#
#     # Define the exact features your model expects
#     expected_features = [
#         'SeniorCitizen', 'tenure', 'MonthlyCharges_log', 'TotalCharges_log',
#         'average_charges_per_month', 'contract_loyalty', 'contract_progress',
#         'ServiceCount', 'charge_tenure_ratio_log', 'security_bundle', 'is_long_contract',
#         'family_flag', 'Contract', 'gender', 'PaperlessBilling',
#         'InternetService_Fiber optic', 'OnlineSecurity_No',
#         'TechSupport_No', 'PaymentMethod_Electronic check',
#         'billing_flag_partial_month'
#     ]
#
#     if os.path.exists(f"{encoders_dir}/ordinal_encoder.pkl"):
#         # INFERENCE MODE
#         ordinal_encoder = joblib.load(f"{encoders_dir}/ordinal_encoder.pkl")
#         ohe = joblib.load(f"{encoders_dir}/ohe_full.pkl")
#         label_encoders = joblib.load(f"{encoders_dir}/label_encoders.pkl")
#
#         # Transform ordinal features
#         x_data_ord = pd.DataFrame(
#             ordinal_encoder.transform(data[ordinal_features]),
#             columns=ordinal_features, index=data.index
#         )
#
#         # Transform binary features
#         x_data_bin = data[binary_features].copy()
#         for col in binary_features:
#             le = label_encoders[col]
#             unique_labels = set(le.classes_)
#             x_data_bin[col] = data[col].apply(lambda x: le.transform([x])[0] if x in unique_labels else -1)
#
#         # Transform nominal features
#         x_data_nom = pd.DataFrame(
#             ohe.transform(data[nominal_features]),
#             columns=ohe.get_feature_names_out(nominal_features),
#             index=data.index
#         )
#
#         # Get numeric features (num_features is now defined above)
#         x_data_num = data[num_features].copy()
#
#         # Combine all features
#         X = pd.concat([x_data_num, x_data_ord, x_data_bin, x_data_nom], axis=1)
#
#         # Select only the expected features
#         available_features = [col for col in expected_features if col in X.columns]
#         missing_features = [col for col in expected_features if col not in X.columns]
#
#         print(f"Available features: {len(available_features)}")
#         print(f"Missing features: {missing_features}")
#
#         # Add missing features as zeros
#         for feature in missing_features:
#             X[feature] = 0
#
#         # Select only the expected features in the correct order
#         X = X[expected_features]
#
#     else:
#         # TRAINING MODE
#         ordinal_encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
#         ohe_full = OneHotEncoder(drop=None, handle_unknown="ignore", sparse_output=False)
#         label_encoders = {}
#
#         x_data_ord = pd.DataFrame(
#             ordinal_encoder.fit_transform(data[ordinal_features]),
#             columns=ordinal_features, index=data.index
#         )
#
#         x_data_bin = data[binary_features].copy()
#         for col in binary_features:
#             le = LabelEncoder()
#             le.fit(data[col])
#             x_data_bin[col] = le.transform(data[col])
#             label_encoders[col] = le
#
#         x_data_nom = pd.DataFrame(
#             ohe_full.fit_transform(data[nominal_features]),
#             columns=ohe_full.get_feature_names_out(nominal_features),
#             index=data.index
#         )
#
#         # Get numeric features (num_features is now defined above)
#         x_data_num = data[num_features].copy()
#         X = pd.concat([x_data_num, x_data_ord, x_data_bin, x_data_nom], axis=1)
#
#         os.makedirs(encoders_dir, exist_ok=True)
#         joblib.dump(ordinal_encoder, f"{encoders_dir}/ordinal_encoder.pkl")
#         joblib.dump(ohe_full, f"{encoders_dir}/ohe_full.pkl")
#         joblib.dump(label_encoders, f"{encoders_dir}/label_encoders.pkl")
#
#         # Save consistent feature order if training
#         joblib.dump(X.columns.tolist(), "../saved_data/feature_names/tree_feature_names.pkl")
#
#         # Select only the expected features
#         available_features = [col for col in expected_features if col in X.columns]
#         missing_features = [col for col in expected_features if col not in X.columns]
#
#         print(f"Available features: {len(available_features)}")
#         print(f"Missing features: {missing_features}")
#
#         # Add missing features as zeros
#         for feature in missing_features:
#             X[feature] = 0
#
#         # Select only the expected features in the correct order
#         X = X[expected_features]
#
#         # Save the final feature order after selection
#         joblib.dump(X.columns.tolist(), "customer_churn_app/feature_order.pkl")
#
#     return X



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