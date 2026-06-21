import pandas as pd

def generate_stats(df: pd.DataFrame, column_types: dict) -> dict:
    """
    Accepts a DataFrame and a dictionary of column type classifications.
    Computes summary metrics for numeric and categorical columns.
    Explicitly detects and reports multi-way ties for most frequent values.
    """
    stats_summary = {
        "numeric": {},
        "categorical": {}
    }
    
    for col_name, col_role in column_types.items():
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
            
        # 2. Process Categorical Columns (With Robust Tie-Handling)
        elif col_role == "categorical":
            value_counts_dict = df[col_name].value_counts().to_dict()
            
            # mode() finds all values that tie for the highest frequency count
            mode_series = df[col_name].mode().dropna()
            
            if mode_series.empty:
                most_frequent = "N/A"
                is_tie = False
            elif len(mode_series) > 1:
                # Option 1: Convert all tied items into a clean Python list
                most_frequent = mode_series.tolist()
                is_tie = True
            else:
                # Single clear winner: extract the string directly
                most_frequent = mode_series.iloc[0]
                is_tie = False
            
            stats_summary["categorical"][col_name] = {
                "value_counts": value_counts_dict,
                "most_frequent": most_frequent,
                "is_tie": is_tie
            }
            
    return stats_summary


def generate_date_stats(df: pd.DataFrame, column_types: dict) -> dict:
    """
    Identifies date columns and computes chronological metrics.
    Handles the edge case where no date columns are present without crashing.
    """
    date_summary = {}
    
    date_cols = [name for name, role in column_types.items() if role == "date" and name in df.columns]
    
    if not date_cols:
        return {"status": "No date columns found", "trends": {}}
        
    for col_name in date_cols:
        temp_date_series = pd.to_datetime(df[col_name], format='ISO8601')
        
        earliest_date = temp_date_series.min().strftime('%Y-%m-%d')
        latest_date = temp_date_series.max().strftime('%Y-%m-%d')
        
        monthly_trends = {}
        numeric_cols = [name for name, role in column_types.items() if role == "numeric" and name in df.columns]
        
        if numeric_cols:
            month_periods = temp_date_series.dt.to_period('M')
            for num_col in numeric_cols:
                grouped = df.groupby(month_periods)[num_col].sum()
                monthly_trends[num_col] = {str(period): float(val) for period, val in grouped.items()}
        
        date_summary[col_name] = {
            "date_range": {
                "start": earliest_date,
                "end": latest_date
            },
            "monthly_totals": monthly_trends
        }
        
    return date_summary