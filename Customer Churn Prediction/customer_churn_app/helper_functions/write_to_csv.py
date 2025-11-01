import os


def write_to_csv(df):
    file_path = 'customer_churn_app/customer_data.csv'

    # Check if the file exists
    if not os.path.exists(file_path):
        df.to_csv(file_path, mode='w', header=False, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)
