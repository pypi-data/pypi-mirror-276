import pandas as pd

def load_data(file_path):
    """
    Load a csv file and return a pandas DataFrame.
    """
    return pd.read_csv(file_path)

def save_data(df, file_path):
    """
    Save a pandas DataFrame to a csv file.
    """
    df.to_csv(file_path, index=False)