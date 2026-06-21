from data_processing.loader import load_csv

print("--- TESTING DATA LOADER MODULE ---")

# Test 1: Successful Load of Mock Data
print("\nTest 1: Loading valid mock sales data...")
try:
    data_path = "sample_data/mock_sales_data.csv"
    df = load_csv(data_path)
    print("✅ Success! File loaded perfectly.")
    print("Here are the first 3 rows of your dataset:")
    print(df.head(3))
except Exception as e:
    print(f"❌ Test 1 Failed unexpectedly: {e}")

# Test 2: Error Handling for a Non-Existent File
print("\nTest 2: Testing error handling for a missing file...")
try:
    missing_path = "sample_data/ghost_file.csv"
    df_ghost = load_csv(missing_path)
    print("❌ Test 2 Failed: The function should have thrown an error but didn't.")
except FileNotFoundError as e:
    print(f"✅ Success! Caught expected error message:\n   {e}")
except Exception as e:
    print(f"❌ Test 2 Failed: Caught a wrong exception type: {e}")

print("\n--- TEST RUN COMPLETED ---")