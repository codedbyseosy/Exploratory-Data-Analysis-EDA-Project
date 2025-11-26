```python
# Import necessary libraries
import numpy as np
import pandas as pd


def reduce_labels(data):
    """
    Simplifies service-related columns by replacing 'No service' labels with 'No'

    Args:
        data: DataFrame containing telecom customer data

    Returns:
        DataFrame with new categorised columns
    """
    # Define columns and values to replace
    cols_to_edit = {
        'MultipleLines': 'No phone service',
        ('OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
         'StreamingMovies'): 'No internet service'
    }

    # Replace "No phone/internet service" with "No" in specified columns
    for key, value in cols_to_edit.items():
        if isinstance(key, tuple):
            # Handle multiple columns with same replacement value
            for col in key:
                data[f"{col}_categorised"] = data[col].replace(value, 'No')
        else:
            # Handle single column replacement
            data[f"{key}_categorised"] = data[key].replace(value, 'No')

    return data


def bin_tenure(data):
    """
    Categorises customer tenure into meaningful bins

    Args:
        data: DataFrame with 'tenure' column

    Returns:
        DataFrame with new 'tenure_bin' column
    """
    # Defining the custom bins for categorising customer tenure (in months)
    bins = [0, 24, 48, 73]

    # Defining the corresponding labels for each bin
    labels = ['Short term', 'Mid term', 'Long term']

    # Categorising 'tenure' values into bins
    data['tenure_bin'] = pd.cut(data['tenure'], bins=bins, labels=labels, right=False)

    return data


def determine_plans(plan):
    """
    Determines pricing tier based on monthly charge amount

    Args:
        plan: Monthly charge value

    Returns:
        String representing pricing tier
    """
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
    """
    Categorises customers into monthly pricing tiers

    Args:
        data: DataFrame with 'MonthlyCharges' column

    Returns:
        DataFrame with new 'monthly_pricing_tiers' column
    """
    # Apply the function to create a new column 'monthly_pricing_tiers'
    data['monthly_pricing_tiers'] = data['MonthlyCharges'].apply(determine_plans)

    return data


def charge_diff(data):
    """
    Calculates the difference between total charges and expected charges (monthly * tenure)

    Args:
        data: DataFrame with 'TotalCharges' and 'MonthlyCharges' columns

    Returns:
        DataFrame with new 'charge_diff' column
    """
    # Creating new column to check for discrepancies
    data['charge_diff'] = data['TotalCharges'] - (data['MonthlyCharges'] * data['tenure'])

    return data


def billing_issue(row):
    """
    Identifies billing anomalies based on charge difference

    Args:
        row: DataFrame row containing charge_diff and MonthlyCharges

    Returns:
        String describing billing status
    """
    charge_diff = row['charge_diff']
    monthly_charge = row['MonthlyCharges']

    # If a customer joined/left mid-month (small difference)
    if abs(charge_diff) < (0.5 * monthly_charge):
        return 'partial_month'

    # If a customer consistently paid less (negative difference within range)
    elif (-1 * monthly_charge) <= charge_diff <= (-0.5 * monthly_charge):
        return 'discount'

    # If something is a billing issue (large discrepancy)
    elif abs(charge_diff) > monthly_charge:
        return 'billing_issue'

    # Perfectly aligned payments
    elif charge_diff == 0:
        return 'ok'

    return 'ok'  # default case for minor differences


def billing_flag(data):
    """
    Applies billing issue detection to entire dataset

    Args:
        data: DataFrame with charge_diff and MonthlyCharges columns

    Returns:
        DataFrame with new 'billing_flag' column
    """
    # Apply row-wise billing issue detection
    data['billing_flag'] = data.apply(billing_issue, axis=1)

    return data


def average_charges_per_month(data):
    """
    Calculates average monthly charges (total charges divided by tenure)

    Args:
        data: DataFrame with 'TotalCharges' and 'tenure' columns

    Returns:
        DataFrame with new 'average_charges_per_month' column
    """
    # Create a new column to calculate the average charges per month
    data['average_charges_per_month'] = (data['TotalCharges'] / data['tenure']).round(2)
    return data


def contract_loyalty(data):
    """
    Identifies loyal customers with long-term contracts and tenure > 12 months

    Args:
        data: DataFrame with 'Contract' and 'tenure' columns

    Returns:
        DataFrame with new 'contract_loyalty' column
    """
    # Create new feature 'contract_loyalty'
    data['contract_loyalty'] = (
            (data['Contract'] != 'Month-to-month') &
            (data['tenure'] > 12)).astype(int)
    return data


def contract_length(contract):
    """
    Converts contract type to numerical length in months

    Args:
        contract: String representing contract type

    Returns:
        Integer representing contract length in months
    """
    if contract == 'Month-to-month':  # Month-to-month - 1 month
        return 1
    elif contract == 'One year':  # One year contract - 12 months
        return 12
    elif contract == 'Two year':  # Two year contract - 24 months
        return 24


def contract_progress(data):
    """
    Calculates how far a customer has progressed into their contract

    Args:
        data: DataFrame with 'Contract' and 'tenure' columns

    Returns:
        DataFrame with new 'contract_progress' column
    """
    # Apply the function to create new column "contract_length"
    data['contract_length'] = data['Contract'].apply(contract_length)

    # Create new column to calculate how far a customer has progressed into their contract
    data['contract_progress'] = (data['tenure'] / data['contract_length']).round(2)

    return data


def service_count(data):
    """
    Counts the number of services each customer is subscribed to

    Args:
        data: DataFrame with service-related columns

    Returns:
        DataFrame with new 'ServiceCount' column
    """
    # Define the list of service-related columns to analyse
    service_cols = ['PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                    'TechSupport', 'StreamingTV', 'StreamingMovies']

    # Create a new column to count the number of services a customer is subscribed to
    data['ServiceCount'] = (data[service_cols] == 'Yes').sum(axis=1)

    return data


def charge_tenure_ratio(data):
    """
    Creates charge-to-tenure ratio and its log transformation

    Args:
        data: DataFrame with 'MonthlyCharges' and 'tenure' columns

    Returns:
        DataFrame with new ratio columns
    """
    # Create a new feature: charge-to-tenure ratio
    data['charge_tenure_ratio'] = (data['MonthlyCharges'] / (data['tenure'] + 1)).round(2)

    # Apply log transformation to reduce skewness in the ratio
    data['charge_tenure_ratio_log'] = np.log1p(data['charge_tenure_ratio']).round(2)

    return data


def address_skewness(data):
    """
    Applies log transformation to skewed numerical features

    Args:
        data: DataFrame with numerical columns

    Returns:
        DataFrame with transformed columns
    """
    # List of columns with expected skewness
    skewed_list = ['MonthlyCharges', 'TotalCharges', 'charge_tenure_ratio']

    # Apply log transformation to each skewed column
    for i in skewed_list:
        data[i] = np.log1p(data[i])

    return data


def high_engagement_loyalty(data):
    """
    Identifies highly engaged loyal customers (many services + long contract)

    Args:
        data: DataFrame with 'ServiceCount' and 'contract_length' columns

    Returns:
        DataFrame with new 'high_engagement_loyalty' column
    """
    # Create new feature called 'high_engagement_loyalty'
    data['high_engagement_loyalty'] = (
            (data['ServiceCount'] >= 5) &
            (data['contract_length'] >= 12)).astype(int)
    return data


def additional_features(data):
    """
    Creates multiple additional engineered features for analysis

    Args:
        data: DataFrame with customer data

    Returns:
        DataFrame with multiple new feature columns
    """
    # High risk: month-to-month contracts with high monthly charges
    data["high_risk_contract"] = ((data["Contract"] == "Month-to-month") &
                                  (data["MonthlyCharges"] > 80)).astype(int)

    # Recent high charge: new customers with high monthly charges
    data["recent_high_charge"] = ((data["tenure"] < 12) & (data["MonthlyCharges"] > 90)).astype(int)

    # Automatic payment methods
    auto_methods = ["Bank transfer (automatic)", "Credit card (automatic)"]
    data["is_auto_pay"] = data["PaymentMethod"].isin(auto_methods).astype(int)

    # Electronic check payment method
    data["is_electronic_check"] = (data["PaymentMethod"] == "Electronic check").astype(int)

    # Security bundle: count of security-related services
    data["security_bundle"] = (
            (data["OnlineSecurity"] == "Yes").astype(int) +
            (data["OnlineBackup"] == "Yes").astype(int) +
            (data["DeviceProtection"] == "Yes").astype(int) +
            (data["TechSupport"] == "Yes").astype(int)
    )

    # Entertainment bundle: has both streaming services
    data["entertainment_bundle"] = ((data["StreamingTV"] == "Yes") &
                                    (data["StreamingMovies"] == "Yes")).astype(int)

    # Paperless billing with autopay
    data["paperless_autopay"] = ((data["PaperlessBilling"] == "Yes") &
                                 (data["is_auto_pay"] == 1)).astype(int)

    # Senior citizens with long tenure
    data["senior_loyal"] = ((data["SeniorCitizen"] == 1) &
                            (data["tenure"] > 24)).astype(int)

    # Long-term contracts (not month-to-month)
    data["is_long_contract"] = data["Contract"].isin(["One year", "Two year"]).astype(int)

    # Family indicator: has partner or dependents
    data["family_flag"] = ((data["Partner"] == "Yes") |
                           (data["Dependents"] == "Yes")).astype(int)
    return data


```