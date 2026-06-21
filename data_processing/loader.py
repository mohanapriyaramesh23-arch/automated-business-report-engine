import os
import pandas as pd

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Accepts a path to a CSV file and loads it into a Pandas DataFrame.
    Handles missing files, empty data, and invalid file formats gracefully.
    """
    # 1. Check if the file physically exists on the disk
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file at '{file_path}' does not exist.")
        
    try:
        # 2. Attempt to read the CSV file using pandas
        df = pd.read_csv(file_path)
        
        # 3. Check if the file is empty (has no rows of data)
        if df.empty:
            raise ValueError(f"Error: The file at '{file_path}' is completely empty.")
            
        return df

    except pd.errors.EmptyDataError:
        raise ValueError(f"Error: The file at '{file_path}' contains no data or headers.")
    except pd.errors.ParserError:
        raise TypeError(f"Error: The file at '{file_path}' is not a valid CSV format or is corrupted.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while loading the file: {str(e)}")