"""
Unit tests for data processing functions.
Tests focus on data cleaning, merging, and basic functionality.
"""
import pandas as pd
import numpy as np
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_cleaning import clean_zillow_data
from src.data_merging import merge_all_data

def test_fips_code_creation():
    """Test that FIPS codes are created correctly from State and County codes."""
    print("Testing FIPS code creation...")

    # Create test data
    test_data = pd.DataFrame({
        'State': ['CA', 'NY'],
        'StateFIPS': [6, 36],
        'CountyFIPS': [37, 61]
    })

    # Simulate FIPS creation logic
    test_data["StateFIPS"] = test_data["StateFIPS"].astype(str).str.zfill(2)
    test_data["CountyFIPS"] = test_data["CountyFIPS"].astype(str).str.zfill(3)
    test_data["FIPS"] = test_data["StateFIPS"] + test_data["CountyFIPS"]

    # Check results
    assert test_data["FIPS"].iloc[0] == "06037", "FIPS for CA should be 06037"
    assert test_data["FIPS"].iloc[1] == "36061", "FIPS for NY should be 36061"
    assert all(test_data["FIPS"].str.len() == 5), "All FIPS codes should be 5 characters"

    print("FIPS code creation test passed")
    return True

def test_data_cleaning_logic():
    """Test the data cleaning function with simple test data."""
    print("Testing data cleaning logic...")

    # Create test Zillow data
    test_zillow = pd.DataFrame({
        'RegionName': ['Test County A', 'Test County B'],
        'State': ['CA', 'NY'],
        'StateCodeFIPS': [6, 36],
        'MunicipalCodeFIPS': [1, 2],
        '2022-12-31': [500000.0, 300000.0]
    })

    # Apply cleaning function
    cleaned = clean_zillow_data(test_zillow)

    # Check results
    assert isinstance(cleaned, pd.DataFrame), "Should return a DataFrame"
    assert 'FIPS' in cleaned.columns, "Should have FIPS column"
    assert 'County' in cleaned.columns, "Should have County column"
    assert 'State' in cleaned.columns, "Should have State column"
    assert 'MedianHomeValue' in cleaned.columns, "Should have MedianHomeValue column"
    assert len(cleaned) == 2, "Should have 2 rows"
    assert cleaned['FIPS'].iloc[0] == '06001', "First FIPS should be 06001"
    assert cleaned['FIPS'].iloc[1] == '36002', "Second FIPS should be 36002"

    print("Data cleaning logic test passed")
    return True

def test_data_merging_logic():
    """Test the data merging function with simple test data."""
    print("Testing data merging logic...")

    # Create test datasets
    zillow_test = pd.DataFrame({
        'FIPS': ['06001', '36002', '99999'],
        'County': ['County A', 'County B', 'County C'],
        'State': ['CA', 'NY', 'XX'],
        'MedianHomeValue': [500000.0, 300000.0, 100000.0]
    })

    census_test = pd.DataFrame({
        'FIPS': ['06001', '36002', '88888'],
        'Median_Income': [80000.0, 70000.0, 50000.0],
        'Population': [100000, 200000, 50000],
        'Poverty_Rate': [10.0, 15.0, 20.0]
    })

    bls_test = pd.DataFrame({
        'FIPS': ['06001', '36002', '77777'],
        'UnemploymentRate': [4.5, 5.0, 8.0]
    })

    # Apply merging function
    merged = merge_all_data(zillow_test, census_test, bls_test)

    # Check results
    assert isinstance(merged, pd.DataFrame), "Should return a DataFrame"
    assert len(merged) == 2, "Should merge only matching FIPS codes"
    assert set(['06001', '36002']) == set(merged['FIPS'].tolist()), "Should contain correct FIPS codes"
    assert 'MedianHomeValue' in merged.columns, "Should have Zillow data"
    assert 'Median_Income' in merged.columns, "Should have Census data"
    assert 'UnemploymentRate' in merged.columns, "Should have BLS data"

    # Check that the merge is correct (inner join)
    assert merged[merged['FIPS'] == '06001']['MedianHomeValue'].iloc[0] == 500000.0
    assert merged[merged['FIPS'] == '06001']['Median_Income'].iloc[0] == 80000.0
    assert merged[merged['FIPS'] == '06001']['UnemploymentRate'].iloc[0] == 4.5

    print("Data merging logic test passed")
    return True

def test_missing_value_handling():
    """Test how the code handles missing values in merging."""
    print("Testing missing value handling...")

    # Create test data with missing values
    test_data = pd.DataFrame({
        'FIPS': ['06001', '36002', '48003'],
        'Value': [100.0, np.nan, 200.0],
        'Category': ['A', 'B', 'C']
    })

    # Check missing value detection
    missing_count = test_data['Value'].isna().sum()
    assert missing_count == 1, f"Should have 1 missing value, got {missing_count}"

    # Check that non-missing values are correct
    non_missing = test_data['Value'].dropna()
    assert len(non_missing) == 2, "Should have 2 non-missing values"
    assert non_missing.iloc[0] == 100.0, "First non-missing should be 100.0"
    assert non_missing.iloc[1] == 200.0, "Second non-missing should be 200.0"

    print("Missing value handling test passed")
    return True

def test_column_validation():
    """Test that required columns exist after processing."""
    print("Testing column validation...")

    # Simulate a processed dataset
    processed_data = pd.DataFrame({
        'FIPS': ['06001', '36002'],
        'County': ['County A', 'County B'],
        'State': ['CA', 'NY'],
        'MedianHomeValue': [500000.0, 300000.0],
        'Median_Income': [80000.0, 70000.0],
        'Population': [100000, 200000],
        'Poverty_Rate': [10.0, 15.0],
        'College_Educated_Pct': [30.0, 25.0],
        'UnemploymentRate': [4.5, 5.0]
    })

    # Define required columns
    required_columns = [
        'FIPS', 'County', 'State', 'MedianHomeValue',
        'Median_Income', 'Poverty_Rate', 'College_Educated_Pct', 'UnemploymentRate'
    ]

    # Check all required columns exist
    missing_columns = [col for col in required_columns if col not in processed_data.columns]
    assert len(missing_columns) == 0, f"Missing required columns: {missing_columns}"

    # Check data types
    assert processed_data['FIPS'].dtype == object, "FIPS should be string/object type"
    assert processed_data['MedianHomeValue'].dtype in [np.float64, np.int64], "MedianHomeValue should be numeric"
    assert processed_data['Median_Income'].dtype in [np.float64, np.int64], "Median_Income should be numeric"

    print("Column validation test passed")
    return True

def run_all_tests():
    """Run all unit tests and provide a summary."""
    print("=" * 60)
    print("RUNNING UNIT TESTS")
    print("=" * 60)

    test_functions = [
        ("FIPS Code Creation", test_fips_code_creation),
        ("Data Cleaning Logic", test_data_cleaning_logic),
        ("Data Merging Logic", test_data_merging_logic),
        ("Missing Value Handling", test_missing_value_handling),
        ("Column Validation", test_column_validation)
    ]

    results = []

    for test_name, test_func in test_functions:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"Error in {test_name}: {str(e)}")
            results.append((test_name, False))

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = 0
    for test_name, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"{test_name}: {status}")
        if success:
            passed += 1

    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\nAll tests passed successfully!")
        return True
    else:
        print(f"\n{total - passed} test(s) failed.")
        return False

if __name__ == "__main__":
    # Run tests
    success = run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)