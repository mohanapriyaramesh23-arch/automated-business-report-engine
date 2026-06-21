import pandas as pd

def detect_column_types(df: pd.DataFrame) -> dict:
    """
    Analyzes a Pandas DataFrame and classifies each column into one of four roles:
    'numeric', 'categorical', 'date', or 'unique_identifier'.
    Returns a dictionary mapping column names to their detected type roles.
    """
    classifications = {}
    total_rows = len(df)
    
    for column in df.columns:
        col_type = str(df[column].dtype)
        
        # 1. Identify Numeric Columns
        if col_type.startswith('int') or col_type.startswith('float'):
            classifications[column] = "numeric"
            continue
            
        # 2. Check for Date/Time formats (since they load as generic text 'object' types)
        # We try to convert a copy of the column to a date. If it doesn't crash, it's a date!
        try:
            # errors='raise' forces it to fail if it's plain text like a product name
            pd.to_datetime(df[column], errors='raise', format='ISO8601')
            classifications[column] = "date"
            continue
        except (ValueError, TypeError):
            # If it throws an error, it's not a date, so proceed to text evaluations
            pass
            
        # 3. Handle Text/Object Column evaluation
        num_unique_values = df[column].nunique()
        
        # If every single row has a completely unique value, it's an ID
        if num_unique_values == total_rows:
            classifications[column] = "unique_identifier"
        else:
            # If values repeat across rows, it's a grouping category
            classifications[column] = "categorical"
            
    return classifications