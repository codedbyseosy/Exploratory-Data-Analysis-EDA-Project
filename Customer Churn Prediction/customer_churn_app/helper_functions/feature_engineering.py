import numpy as np
import pandas as pd


def reduce_labels(data):
    # Define columns and values to replace
    cols_to_edit = {
        'MultipleLines': 'No phone service',
        ('OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
         'StreamingMovies'): 'No internet service'
    }

    # Replace "No phone/internet service" with "No"
    for key, value in cols_to_edit.items():
        if isinstance(key, tuple):
            for col in key:
                data[f"{col}_categorised"] = data[col].replace(value, 'No')
        else:
            data[f"{key}_categorised"] = data[key].replace(value, 'No')

    return data


def bin_tenure(data):
    # Defining the custom bins for categorising customer tenure (in months)
    bins = [0, 24, 48, 73]

    # Defining the corresponding labels for each bin
    labels = ['Short term', 'Mid term', 'Long term']

    # Categorising 'tenure' values into bins
    data['tenure_bin'] = pd.cut(data['tenure'], bins=bins, labels=labels, right=False)

    return data


def determine_plans(plan):
    # If monthly charge is less than $40 -> Basic plan
    if plan < 40:
        return 'Basic'
    # If monthly charge is between $40 and $70 -> Standard plan
    elif plan < 70:
        return 'Standard'
    # If monthly charge is between $70 and $95 -> Premium plan
    elif plan < 95:
        return 'Premium'
    # If $95 or more -> Platinum plan
    else:
        return 'Platinum'


def monthly_plans(data):
    # Apply the function to create a new column 'monthly_pricing_tiers'
    data['monthly_pricing_tiers'] = data['MonthlyCharges'].apply(determine_plans)

    return data


def charge_diff(data):
    # Creating new column to check for discrepancies
    data['charge_diff'] = data['TotalCharges'] - (data['MonthlyCharges'] * data['tenure'])

    return data


def billing_issue(row):
    charge_diff = row['charge_diff']
    monthly_charge = row['MonthlyCharges']

    # If a customer joined/left mid-month
    if abs(charge_diff) < (0.5 * monthly_charge):
        return 'partial_month'

    # If a customer consistently paid less
    elif (-1 * monthly_charge) <= charge_diff <= (-0.5 * monthly_charge):
        return 'discount'

    # If something is a billing issue
    elif abs(charge_diff) > monthly_charge:
        return 'billing_issue'

    # Perfectly aligned
    elif charge_diff == 0:
        return 'ok'

    return 'ok'  # default match


def billing_flag(data):
    # Apply row-wise
    data['billing_flag'] = data.apply(billing_issue, axis=1)

    return data


def average_charges_per_month(data):
    # Create a new column to calculate the average charges per month
    data['average_charges_per_month'] = (data['TotalCharges'] / data['tenure']).round(2)
    return data


def contract_loyalty(data):
    # Create new feature 'contract_loyalty'
    data['contract_loyalty'] = (
            (data['Contract'] != 'Month-to-month') &
            (data['tenure'] > 12)).astype(int)
    return data


def contract_length(contract):
    if contract == 'Month-to-month':     # Month-to-moth - 1 month
        return 1
    elif contract == 'One year':         # One year contract - 12 months
        return 12
    elif contract == 'Two year':         # Two year contract - 24 months
        return 24


def contract_progress(data):
    # Apply the function to create new column "contract_length"
    data['contract_length'] = data['Contract'].apply(contract_length)

    # Create new column to calculate how far a customer has progressed into their contract
    data['contract_progress'] = (data['tenure'] / data['contract_length']).round(2)

    return data


def service_count(data):
    # Define the list of service-related columns to analyse
    service_cols = ['PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                    'TechSupport', 'StreamingTV', 'StreamingMovies']

    # Create a new column to count the number of services a customer is subscribed to
    data['ServiceCount'] = (data[service_cols] == 'Yes').sum(axis=1)

    return data


def charge_tenure_ratio(data):
    # Create a new feature: charge-to-tenure ratio
    data['charge_tenure_ratio'] = (data['MonthlyCharges'] / (data['tenure'] + 1)).round(2)

    # Apply log transformation to reduce skewness in the ratio
    data['charge_tenure_ratio_log'] = np.log1p(data['charge_tenure_ratio']).round(2)

    return data


def address_skewness(data): # add this in after making charge_tenure_ratio
    skewed_list = ['MonthlyCharges', 'TotalCharges', 'charge_tenure_ratio']

    for i in skewed_list:
        data[i] = np.log1p(data[i])

    return data


def high_engagement_loyalty(data):
    # Create new feature called 'high_engagement_loyalty'
    data['high_engagement_loyalty'] = (
            (data['ServiceCount'] >= 5) &
            (data['contract_length'] >= 12)).astype(int)
    return data


def additional_features(data):
    data["high_risk_contract"] = ((data["Contract"] == "Month-to-month") &
                                     (data["MonthlyCharges"] > 80)).astype(int)

    data["recent_high_charge"] = ((data["tenure"] < 12) & (data["MonthlyCharges"] > 90)).astype(int)

    auto_methods = ["Bank transfer (automatic)", "Credit card (automatic)"]
    data["is_auto_pay"] = data["PaymentMethod"].isin(auto_methods).astype(int)

    data["is_electronic_check"] = (data["PaymentMethod"] == "Electronic check").astype(int)

    data["security_bundle"] = (
            (data["OnlineSecurity"] == "Yes").astype(int) +
            (data["OnlineBackup"] == "Yes").astype(int) +
            (data["DeviceProtection"] == "Yes").astype(int) +
            (data["TechSupport"] == "Yes").astype(int)
    )

    data["entertainment_bundle"] = ((data["StreamingTV"] == "Yes") &
                                       (data["StreamingMovies"] == "Yes")).astype(int)

    data["paperless_autopay"] = ((data["PaperlessBilling"] == "Yes") &
                                    (data["is_auto_pay"] == 1)).astype(int)

    data["senior_loyal"] = ((data["SeniorCitizen"] == 1) &
                               (data["tenure"] > 24)).astype(int)

    data["is_long_contract"] = data["Contract"].isin(["One year", "Two year"]).astype(int)

    data["family_flag"] = ((data["Partner"] == "Yes") |
                              (data["Dependents"] == "Yes")).astype(int)
    return data
