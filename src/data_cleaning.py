"""
Data cleaning module for the project.
Functions to clean and prepare data for analysis.
"""
import pandas as pd

# Import from config
from config import LATEST_DATE

def clean_zillow_data(zillow_df):
    """
    Clean and prepare Zillow home value data.

    Args:
        zillow_df: Raw Zillow home value data

    Returns:
        pandas.DataFrame: Cleaned Zillow data with FIPS codes and home values
    """
    print("Cleaning Zillow data...")

    # Select relevant columns
    zillow_clean = zillow_df[
        ["RegionName", "State", "StateCodeFIPS", "MunicipalCodeFIPS", LATEST_DATE]
    ].copy()

    # Rename columns
    zillow_clean.columns = ["County", "State", "StateFIPS", "CountyFIPS", "MedianHomeValue"]

    # Create FIPS code
    zillow_clean["StateFIPS"] = zillow_clean["StateFIPS"].astype(str).str.zfill(2)
    zillow_clean["CountyFIPS"] = zillow_clean["CountyFIPS"].astype(str).str.zfill(3)
    zillow_clean["FIPS"] = zillow_clean["StateFIPS"] + zillow_clean["CountyFIPS"]
    zillow_clean["FIPS"] = zillow_clean["FIPS"].astype(str)

    # Select final columns and drop missing values
    zillow_final = zillow_clean[["FIPS", "County", "State", "MedianHomeValue"]].dropna()

    print(f"Zillow data cleaned: {zillow_final.shape[0]} counties")
    return zillow_final