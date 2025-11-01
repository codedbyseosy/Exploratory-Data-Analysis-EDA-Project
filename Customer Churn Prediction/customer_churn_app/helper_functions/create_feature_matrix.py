# from helper_functions.feature_engineering import (reduce_labels, bin_tenure, monthly_plans, charge_diff, billing_flag, average_charges_per_month,
#                                                                      contract_loyalty, contract_length, contract_progress,
#                                                                      service_count, charge_tenure_ratio, address_skewness,
#                                                                      high_engagement_loyalty, additional_features)
# import numpy as np

from helper_functions.feature_engineering import (reduce_labels, bin_tenure, monthly_plans, charge_diff, billing_flag, average_charges_per_month,
                                                                     contract_loyalty, contract_length, contract_progress,
                                                                     service_count, charge_tenure_ratio, address_skewness,
                                                                     high_engagement_loyalty, additional_features)
import numpy as np
import pandas as pd


def create_feature_matrix(data):
    dataset = reduce_labels(data)
    dataset = bin_tenure(dataset)
    dataset = monthly_plans(dataset)
    dataset = charge_diff(dataset)
    dataset = billing_flag(dataset)
    dataset = average_charges_per_month(dataset)
    dataset = contract_loyalty(dataset)
    dataset['contract_length'] = dataset['Contract'].apply(contract_length)
    dataset = contract_progress(dataset)
    dataset = service_count(dataset)
    dataset = charge_tenure_ratio(dataset)
    dataset = address_skewness(dataset)
    dataset = high_engagement_loyalty(dataset)
    dataset = additional_features(dataset)
    dataset = dataset.dropna()

    # Create the log features that your model expects
    dataset['MonthlyCharges_log'] = np.log1p(dataset['MonthlyCharges'])
    dataset['TotalCharges_log'] = np.log1p(dataset['TotalCharges'])

    # Remove only the raw columns
    features_to_remove = ['customerID', 'MonthlyCharges', 'TotalCharges', 'charge_diff', 'charge_tenure_ratio', 'contract_length']
    X_untransformed = dataset.drop(columns=features_to_remove, axis=1)

    return X_untransformed