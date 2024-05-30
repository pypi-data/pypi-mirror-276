# json_flattener/flattener.py
import pandas as pd

def flatten_json(json_data):
    """
    Flattens a list of JSON objects.

    Parameters:
    json_data (list): A list of JSON objects.

    Returns:
    pandas.DataFrame: A flattened DataFrame.
    """
    df = pd.json_normalize(json_data)
    return df
