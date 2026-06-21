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
            value_counts_dict = df[col_name].value_counts().to_dict()
            mode_series = df[col_name].mode().dropna()
            most_frequent = mode_series.iloc[0] if not mode_series.empty else "N/A"
            
            stats_summary["categorical"][col_name] = {
                "value_counts": value_counts_dict,
                "most_frequent": most_frequent
            }
            
    return stats_summary


def generate_date_stats(df: pd.DataFrame, column_types: dict) -> dict:
    """
    Identifies date columns and computes chronological metrics.
    Handles the edge case where no date columns are present without crashing.
    """
    date_summary = {}
    
    # Track down if any column is explicitly classified as a date
    date_cols = [name for name, role in column_types.items() if role == "date" and name in df.columns]
    
    # Edge case: If no date column is discovered, return a clear structured message safely
    if not date_cols:
        return {"status": "No date columns found", "trends": {}}
        
    for col_name in date_cols:
        # Create a clean, temporary Series explicitly converted to Datetime objects
        temp_date_series = pd.to_datetime(df[col_name], format='ISO8601')
        
        # Calculate boundaries and convert them to standard readable strings
        earliest_date = temp_date_series.min().strftime('%Y-%m-%d')
        latest_date = temp_date_series.max().strftime('%Y-%m-%d')
        
        # Trend Analysis: Group total Numeric values by month intervals
        # First, bind the clean dates temporarily back into our context calculation
        monthly_trends = {}
        numeric_cols = [name for name, role in column_types.items() if role == "numeric" and name in df.columns]
        
        if numeric_cols:
            # .dt.to_period('M') maps timestamps directly to their calendar month string (e.g. '2026-01')
            month_periods = temp_date_series.dt.to_period('M')
            
            for num_col in numeric_cols:
                # Sum values by month groupings and format the index keys back to clean strings
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