from helper_functions.create_feature_matrix import create_feature_matrix
from helper_functions.encoder import encode_features


# Function to preprocess customer data for churn prediction
def preprocess_data(data):
    """
    Prepares customer data for machine learning prediction by creating features, encoding categroical variables, and
    ensuring consistent format.

    Args:
        data: Raw customer data to be processed.

    Returns:
        final_data: Processed data with exactly 20 numeric features ready for prediction.
    """
    # Step 1: Create additional features from raw data
    data = create_feature_matrix(data)

    # Step 2: Encode categorical variables to numeric format
    data = encode_features(data)

    # Step 3: Ensure data has exactly 20 features for model compatibility
    final_data = data.copy()

    # If there are more than 20 columns, keep only the first 20
    if len(final_data.columns) > 20:
        final_data = final_data.iloc[:, :20]
    # If there are fewer than 20 columns, add zero-filled columns
    elif len(final_data.columns) < 20:
        for i in range(len(final_data.columns), 20):
            final_data[f'Column_{i}'] = 0

    # Step 4: Standardise column names to Column_0 through Colum_19
    final_data.columns = [f'Column_{i}' for i in range(20)]

    # Step 5: Convert all data to float for machine learning model
    final_data = final_data.astype(float)

    # Print confirmation message with shape and data types
    print(f"Preprocessing complete: {final_data.shape}, all dtypes: {final_data.dtypes.unique()}")

    # Step 6: Return refined data
    return final_data




