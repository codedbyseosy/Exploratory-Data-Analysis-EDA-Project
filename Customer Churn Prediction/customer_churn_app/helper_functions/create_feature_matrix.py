from feature_engineering import reduce_labels, bin_tenure, monthly_plans, charge_diff, billing_flag, \
    average_charges_per_month, contract_loyalty, contract_length, contract_progress, service_count, charge_tenure_ratio, \
    address_skewness, high_engagement_loyalty, additional_features


def create_feature_matrix(data):
    # Drop any rows that contain
    dataset = reduce_labels(data)
    dataset = bin_tenure(dataset)
    dataset = monthly_plans(dataset)
    dataset = charge_diff(dataset)
    dataset = billing_flag(dataset)
    dataset = average_charges_per_month(dataset)
    dataset = contract_loyalty(dataset)
    dataset = contract_length(dataset)
    dataset = contract_progress(dataset)
    dataset = service_count(dataset)
    dataset = charge_tenure_ratio(dataset)
    dataset = address_skewness(dataset)
    dataset = address_skewness(dataset)
    dataset = high_engagement_loyalty(dataset)
    dataset = additional_features(dataset)
    dataset = dataset.dropna()

    # Defining the list of features to remove before modeling
    features_to_remove = ['customerID', 'MonthlyCharges', 'TotalCharges', 'charge_diff', 'charge_tenure_ratio',
                          'contract_length']
    # Defining the matrix of features
    X_untransformed = dataset.drop(columns=features_to_remove, axis=1)


    return X_untransformed
