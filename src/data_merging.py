"""
Data merging module for the project.
Functions to merge all datasets into one final dataset.
"""
import pandas as pd

def merge_all_data(zillow_final, census_merged, bls_final):
    """
    Merge Zillow, Census, and BLS data into one comprehensive dataset.

    Args:
        zillow_final: Cleaned Zillow data
        census_merged: Merged Census economic and education data
        bls_final: Processed BLS data

    Returns:
        pandas.DataFrame: Final merged dataset with all variables
    """
    print("Merging all datasets...")

    # Start with Zillow data
    merged_data = zillow_final.copy()

    # Add Census data
    if census_merged is not None:
        merged_data = pd.merge(merged_data, census_merged, on="FIPS", how="inner")
        print(f"Added Census data: {merged_data.shape[0]} counties")

    # Add BLS data
    if bls_final is not None:
        merged_data = pd.merge(
            merged_data,
            bls_final[["FIPS", "UnemploymentRate"]],
            on="FIPS",
            how="inner"
        )
        print(f"Added BLS data: {merged_data.shape[0]} counties")

    # Data quality information
    print(f"Final dataset: {merged_data.shape[0]} counties with complete data")
    print(f"Dataset shape: {merged_data.shape}")

    # Data quality check
    print("Data quality check:")
    missing_values = merged_data.isnull().sum()
    if missing_values.sum() == 0:
        print("No missing values in the dataset")
    else:
        print("Missing values per column:")
        print(missing_values[missing_values > 0])

    return merged_data