from helper_functions.feature_engineering import (reduce_labels, bin_tenure, monthly_plans, charge_diff, billing_flag, average_charges_per_month,
                                                                     contract_loyalty, contract_length, contract_progress,
                                                                     service_count, charge_tenure_ratio, address_skewness,
                                                                     high_engagement_loyalty, additional_features)
import numpy as np

def create_feature_matrix(data):
    """
    Transforms raw customer data into a feature matrix for encoding.

    Applies a series of feature engineering steps to prepare the data for machine learning model consumption.

    Args:
        data: Raw customer data containing demographic, service, and billing information.

    Returns:
        X_untransformed: Feature matrix ready for encoding and transformation
    """

    # Apply sequential feature engineering transformations
    dataset = reduce_labels(data)                   # Simplify categorical labels
    dataset = bin_tenure(dataset)                   # Group tenure into meaningful ranges
    dataset = monthly_plans(dataset)                # Create features from monthly plans
    dataset = charge_diff(dataset)                  # Calculate charge differences
    dataset = billing_flag(dataset)                 # Create billing_related flags
    dataset = average_charges_per_month(dataset)    # Compute average monthly charges
    dataset = contract_loyalty(dataset)             # Generate contract loyalty indicators
    dataset['contract_length'] = dataset['Contract'].apply(contract_length)     # Calculate contract duration
    dataset = contract_progress(dataset)            # Measures progress through contract term
    dataset = service_count(dataset)                # Count total services subscribed
    dataset = charge_tenure_ratio(dataset)          # Compute charge-to-tenure ratio
    dataset = address_skewness(dataset)             # Analyse address distribution patterns
    dataset = high_engagement_loyalty(dataset)      # Identify high-engagement customers
    dataset = additional_features(dataset)          # Add any remaining engineered features

    # Clean data by removing any rows with missing values
    dataset = dataset.dropna()

    # Create logarithmic transformations of monetary features - to prevent skewed distributions
    # and help with the performance
    dataset['MonthlyCharges_log'] = np.log1p(dataset['MonthlyCharges']) # log(1 + MonthlyCharges)
    dataset['TotalCharges_log'] = np.log1p(dataset['TotalCharges']) # log(1 + TotalCharges)

    # Remove raw columns and intermediate features that shouldn't be in the final model
    features_to_remove = ['customerID', 'MonthlyCharges', 'TotalCharges', 'charge_diff', 'charge_tenure_ratio', 'contract_length']
    X_untransformed = dataset.drop(columns=features_to_remove, axis=1)

    return X_untransformed