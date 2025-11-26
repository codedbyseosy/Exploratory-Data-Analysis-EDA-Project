import os


def write_to_csv(df):
    """
        Writes a DataFrame to a CSV file, creating the file with headers if it doesn't exist,
        or appending without headers if the file already exists.

        Args:
            df (pandas.DataFrame): The DataFrame to write to CSV
    """

    # Define the file path for the CSV file
    file_path = 'customer_churn_app/customer_data.csv'

    # Check if the file exists
    if not os.path.exists(file_path):
        # File doesn't exist - create it with data but without header
        # This assumes the first row of df contains what should be the header
        df.to_csv(file_path, mode='w', header=False, index=False)
    else:
        # File exists - append data without repeating the header
        df.to_csv(file_path, mode='a', header=False, index=False)
