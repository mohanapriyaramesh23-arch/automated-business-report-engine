import json
from data_processing.loader import load_csv
from data_processing.column_detector import detect_column_types
from data_processing.stats_generator import generate_stats

print("--- TESTING PART A: BASIC STATISTICS ---")

try:
    # 1. Pipeline execution: Load -> Detect -> Compute Stats
    df = load_csv("sample_data/mock_sales_data.csv")
    column_roles = detect_column_types(df)
    
    computed_stats = generate_stats(df, column_roles)
    
    # 2. Print output using json.dumps to make the nested dictionary pretty and easy to read
    print("✅ Success! Summary statistics generated.\n")
    print(json.dumps(computed_stats, indent=4))
    
except Exception as e:
    print(f"❌ Test Failed unexpectedly: {e}")

print("\n--- TEST RUN COMPLETED ---")