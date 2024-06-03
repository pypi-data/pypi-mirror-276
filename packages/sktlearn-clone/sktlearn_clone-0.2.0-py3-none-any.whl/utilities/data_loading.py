import pandas as pd
import numpy as np

def load_csv(file_path, header='infer', sep=',', index_col=None):
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
    - file_path (str): Path to the CSV file.
    - header (str or int or list of int, default 'infer'): Row(s) to use as the column names of the DataFrame.
    - sep (str, default ','): Delimiter to use.
    - index_col (int or sequence[int], default None): Column(s) to set as index(MultiIndex).

    Returns:
    - DataFrame: The loaded data as a pandas DataFrame.
    """
    return pd.read_csv(file_path, header=header, sep=sep, index_col=index_col)

def load_csv_as_array(file_path, dtype=float, delimiter=','):
    """
    Load data from a CSV file into a NumPy array.

    Args:
    - file_path (str): Path to the CSV file.
    - dtype (data-type, default float): Data type of the resulting array.
    - delimiter (str, default ','): Delimiter to use.

    Returns:
    - ndarray: The loaded data as a NumPy array.
    """
    return np.genfromtxt(file_path, dtype=dtype, delimiter=delimiter)

# # Example usage
# if __name__ == "__main__":
#     csv_file_path = "titanic_fare.csv"
#     dataframe = load_csv(csv_file_path)
#     print("DataFrame:")
#     print(dataframe)

#     array = load_csv_as_array(csv_file_path)
#     print("\nNumPy Array:")
#     print(array)
