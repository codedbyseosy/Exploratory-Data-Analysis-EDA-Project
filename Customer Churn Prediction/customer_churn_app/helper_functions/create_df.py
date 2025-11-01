import pandas as pd


def create_df(field_1, field_2, field_3, field_4, field_5,
              field_6, field_7, field_8, field_9, field_10,
              field_11, field_12, field_13, field_14,
              field_15, field_16, field_17, field_18,
              field_19, field_20):
    data = {
        'customerID': [field_1], # customer_id
        'gender': [field_2], # gender
        'SeniorCitizen': [field_3], # senior_citizen convert to 0 or 1
        'Partner': [field_4], # partner
        'Dependents': [field_5], # dependents
        'tenure': [field_6], # tenure
        'PhoneService': [field_7], # phone_service
        'MultipleLines': [field_8], # multiple_lines
        'InternetService': [field_9], # internet_service
        'OnlineSecurity': [field_10], # online_security
        'OnlineBackup': [field_11], # online_backup
        'DeviceProtection': [field_12], # device_protection
        'TechSupport': [field_13], # tech_support
        'StreamingTV': [field_14], # streaming_tv
        'StreamingMovies': [field_15], # streaming_movies
        'Contract': [field_16], # contract
        'PaperlessBilling': [field_17], # paperless_billing
        'PaymentMethod': [field_18], # payment_method
        'MonthlyCharges': [field_19], # monthly_charges
        'TotalCharges': [field_20] # total_charges
    }
    return pd.DataFrame(data)
