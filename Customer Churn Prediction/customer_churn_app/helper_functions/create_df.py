import pandas as pd


def create_df(field_1, field_2, field_3, field_4, field_5,
              field_6, field_7, field_8, field_9, field_10,
              field_11, field_12, field_13, field_14,
              field_15, field_16, field_17, field_18,
              field_19, field_20):
    """
        Creates a DataFrame with customer information for telecom/churn analysis.

        Args:
            field_1 : str
                Customer ID (customerID)
            field_2 : str
                Gender of customer (gender)
            field_3 : int
                Whether customer is senior citizen (SeniorCitizen)
            field_4 : str
                Whether customer has a partner (Partner)
            field_5 : str
                Whether customer has dependents (Dependents)
            field_6 : int
                Number of months customer has been with company (tenure)
            field_7 : str
                Whether customer has phone service (PhoneService)
            field_8 : str
                Whether customer has multiple lines (MultipleLines)
            field_9 : str
                Type of internet service (InternetService)
            field_10 : str
                Whether customer has online security (OnlineSecurity)
            field_11 : str
                Whether customer has online backup (OnlineBackup)
            field_12 : str
                Whether customer has device protection (DeviceProtection)
            field_13 : str
                Whether customer has tech support (TechSupport)
            field_14 : str
                Whether customer has streaming TV (StreamingTV)
            field_15 : str
                Whether customer has streaming movies (StreamingMovies)
            field_16 : str
                Contract type (Contract)
            field_17 : str
                Whether customer uses paperless billing (PaperlessBilling)
            field_18 : str
                Payment method (PaymentMethod)
            field_19 : float
                Monthly charges amount (MonthlyCharges)
            field_20 : str/float
                Total charges amount (TotalCharges)

        Returns:
            pandas.DataFrame: DataFrame containing the customer data with appropriate column names
        """

    # Create dictionary with field names as keys and input parameters as values
    # This structure maps each field to its corresponding database column
    data = {
        'customerID': [field_1],            # Unique identifier for each customer
        'gender': [field_2],                # Customer's gender (Male/Female)
        'SeniorCitizen': [field_3],         # Binary indicator for senior citizen status (0/1)
        'Partner': [field_4],               # Whether customer has a partner (Yes/No)
        'Dependents': [field_5],            # Whether customer has dependents (Yes/No)
        'tenure': [field_6],                # Number of months customer has stayed with company
        'PhoneService': [field_7],          # Whether customer has phone service (Yes/No)
        'MultipleLines': [field_8],         # Whether customer has multiple phone lines
        'InternetService': [field_9],       # Type of internet service (DSL, Fiber optic, No)
        'OnlineSecurity': [field_10],       # Whether customer has online security service
        'OnlineBackup': [field_11],         # Whether customer has online backup service
        'DeviceProtection': [field_12],     # Whether customer has device protection
        'TechSupport': [field_13],          # Whether customer has tech support
        'StreamingTV': [field_14],          # Whether customer has streaming TV
        'StreamingMovies': [field_15],      # Whether customer has streaming movies
        'Contract': [field_16],             # Contract type (Month-to-month, One year, Two year)
        'PaperlessBilling': [field_17],     # Whether customer uses paperless billing (Yes/No)
        'PaymentMethod': [field_18],        # Payment method (Electronic check, Mailed check, etc.)
        'MonthlyCharges': [field_19],       # Amount charged monthly
        'TotalCharges': [field_20]          # Total amount charged to customer
    }

    # Convert the dictionary to a pandas DataFrame
    return pd.DataFrame(data)
