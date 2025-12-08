"""
Main pipeline for the project.
Runs the entire data processing pipeline from start to end.
"""
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import from local modules
from config import *
from data_loading import *
from data_cleaning import *
from data_merging import *
from analysis import run_analysis

def run_pipeline():
    """
    Run the complete data processing pipeline.

    Returns:
        pandas.DataFrame: Final merged dataset if successful, None otherwise
    """
    print("STARTING DATA PROCESSING PIPELINE")

    # Setup
    warnings.filterwarnings("ignore")
    plt.style.use(PLOT_STYLE)
    sns.set_palette(SEABORN_PALETTE)
    pd.set_option("display.max_columns", PD_DISPLAY_MAX_COLUMNS)
    print("Libraries imported and configured")

    # Step 1: Load data
    print("STEP 1: LOADING DATA")

    try:
        zillow_df = load_zillow_data()
        print(f"Zillow data sample:")
        print(zillow_df[['RegionName', 'State', '2022-12-31']].head())
    except Exception as e:
        print(f"Failed to load Zillow data: {e}")
        return None

    try:
        bls_final = load_bls_data()
        print(f"BLS data sample:")
        print(bls_final.head())
    except Exception as e:
        print(f"Failed to load BLS data: {e}")
        return None

    try:
        census_econ = load_census_economic_data()
        census_edu = load_census_education_data()

        if census_econ is not None and census_edu is not None:
            census_merged = pd.merge(census_econ, census_edu, on="FIPS", how="inner")
            print(f"Census data merged: {census_merged.shape[0]} counties")
            print(f"Census data sample:")
            print(census_merged.head())
        else:
            print("Failed to load Census data")
            return None
    except Exception as e:
        print(f"Failed to load Census data: {e}")
        return None

    # Step 2: Clean data
    print("STEP 2: CLEANING DATA")

    try:
        zillow_final = clean_zillow_data(zillow_df)
        print(f"Cleaned Zillow data sample:")
        print(zillow_final.head())
    except Exception as e:
        print(f"Failed to clean Zillow data: {e}")
        return None

    # Step 3: Merge data
    print("STEP 3: MERGING DATA")

    try:
        merged_data = merge_all_data(zillow_final, census_merged, bls_final)
        print(f"Merged data sample:")
        print(merged_data.head())
    except Exception as e:
        print(f"Failed to merge data: {e}")
        return None

    # Step 4: Run analysis
    print("STEP 4: RUNNING ANALYSIS")

    try:
        results = run_analysis(merged_data)
        print("Analysis completed successfully")
    except Exception as e:
        print(f"Analysis failed: {e}")
        return None

    print("PIPELINE COMPLETED SUCCESSFULLY")

    return merged_data

if __name__ == "__main__":
    print("US COUNTY-LEVEL HOUSING MARKET ANALYSIS")
    print("This pipeline will:")
    print("1. Load data from Zillow, BLS, and Census API")
    print("2. Clean and prepare the data")
    print("3. Merge all datasets")
    print("4. Perform statistical analysis")
    print("5. Create visualizations")

    result = run_pipeline()
