import pandas as pd


def load_raw_dataset(path):
    """
    Load the raw CSV file as a pandas DataFrame.
    """
    df = pd.read_csv(path)
    return df


def drop_unwanted_columns(df, columns_to_drop):
    """
    Drop specified columns if they exist in the DataFrame.
    """
    columns_present = [col for col in columns_to_drop if col in df.columns]
    return df.drop(columns=columns_present)


def impute_mean_inplace(df, column):
    """
    Fill NaN values in the specified column with its mean.
    Returns the mean value used.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame.")
    
    mean_val = df[column].mean() # Calculate mean
    df[column] = df[column].fillna(mean_val) # Impute NaNs with mean
    return mean_val

def save_processed_dataset(df, path):
    """
    Save cleaned DataFrame to CSV without the index.
    """
    df.to_csv(path, index=False)
