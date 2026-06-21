import json
from data_processing.loader import load_csv
from data_processing.column_detector import detect_column_types
from data_processing.stats_generator import generate_date_stats

print("--- TESTING PART B: TIMELINE & TREND STATISTICS ---")

try:
    df = load_csv("sample_data/mock_sales_data.csv")
    column_roles = detect_column_types(df)
    
    # Test 1: Standard Execution with Date Columns
    print("\nTest 1: Analyzing timeline features for valid date arrays...")
    date_metrics = generate_date_stats(df, column_roles)
    print(json.dumps(date_metrics, indent=4))
    
    # Test 2: Edge Case Evaluation (No Date Flag Provided)
    print("\nTest 2: Verifying safety behaviors when date features are absent...")
    fake_roles = {name: ("numeric" if role == "numeric" else "categorical") for name, role in column_roles.items()}
    edge_metrics = generate_date_stats(df, fake_roles)
    print(json.dumps(edge_metrics, indent=4))
    print("\n✅ Success! Edge case caught dynamically without raising a system crash.")
    
except Exception as e:
    print(f"❌ Test Failed unexpectedly: {e}")

print("\n--- TEST RUN COMPLETED ---")