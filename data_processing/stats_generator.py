import pandas as pd

def generate_stats(df: pd.DataFrame, column_types: dict) -> dict:
    """
    Accepts a DataFrame and a dictionary of column type classifications.
    Computes summary metrics for numeric and categorical columns.
    """
    stats_summary = {
        "numeric": {},
        "categorical": {}
    }
    
    for col_name, col_role in column_types.items():
        # Ensure the column actually exists in the DataFrame to avoid crashes
        if col_name not in df.columns:
            continue
            
        # 1. Process Numeric Columns
        if col_role == "numeric":
            stats_summary["numeric"][col_name] = {
                "total": float(df[col_name].sum()),
                "average": float(df[col_name].mean()),
                "min": float(df[col_name].min()),
                "max": float(df[col_name].max())
            }
            
        # 2. Process Categorical Columns
        elif col_role == "categorical":
            # value_counts() returns a series of unique values and their frequencies.
            # We convert it to a standard dictionary.
            value_counts_dict = df[col_name].value_counts().to_dict()
            
            # mode() finds the most frequent value. We use .dropna() to ignore nulls.
            mode_series = df[col_name].mode().dropna()
            most_frequent = mode_series.iloc[0] if not mode_series.empty else "N/A"
            
            stats_summary["categorical"][col_name] = {
                "value_counts": value_counts_dict,
                "most_frequent": most_frequent
            }
            
    return stats_summary