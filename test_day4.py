from data_processing.loader import load_csv
from data_processing.column_detector import detect_column_types

print("--- TESTING COLUMN TYPE DETECTOR MODULE ---")

try:
    # 1. Load the mock data using our Day 3 loader module
    data_path = "sample_data/mock_sales_data.csv"
    df = load_csv(data_path)
    print("✅ Step 1: Mock data loaded successfully.")
    
    # 2. Feed the DataFrame into our Day 4 detector module
    detected_types = detect_column_types(df)
    print("✅ Step 2: Columns classified successfully.\n")
    
    # 3. Print the results out structurally
    print("--- DETECTED COLUMN ROLES ---")
    for col_name, col_role in detected_types.items():
        print(f"• Column: '{col_name}' -> Classified as: {col_role.upper()}")
        
except Exception as e:
    print(f"❌ Test Failed unexpectedly: {e}")

print("\n--- TEST RUN COMPLETED ---")