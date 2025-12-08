"""
Data loading module for the project.
Functions to load data from Zillow, BLS, and Census API.
"""
import os
import pandas as pd
from census import Census
from dotenv import load_dotenv

# Import from config
from config import *

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
CENSUS_API_KEY = os.getenv(CENSUS_API_KEY_VAR)
if not CENSUS_API_KEY:
    raise ValueError("CENSUS_API_KEY not found. Please add it to .env file")

census_client = Census(CENSUS_API_KEY)

def load_zillow_data():
    """
    Load Zillow home value data from URL.

    Returns:
        pandas.DataFrame: Raw Zillow home value data
    """
    print("Loading Zillow home value data...")
    zillow_df = pd.read_csv(ZILLOW_URL)
    print(f"Zillow data loaded: {zillow_df.shape[0]} counties, {zillow_df.shape[1]} columns")
    return zillow_df

def load_bls_data():
    """
    Load BLS unemployment data from Google Sheets.

    Returns:
        pandas.DataFrame: Processed BLS data with FIPS codes and unemployment rates
    """
    print("Loading BLS unemployment data...")

    # Read data from Google Sheets
    df = pd.read_csv(BLS_DATA_URL, skiprows=1)
    df = df.iloc[:, :9]

    # Rename columns
    df.columns = [
        "LAUS", "StateFIPS", "CountyFIPS", "CountyName", "Year",
        "LaborForce", "Employed", "Unemployed", "UnemploymentRate"
    ]

    # Filter for 2022 and convert types
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df[df["Year"] == CENSUS_YEAR].copy()

    numeric_cols = ["LaborForce", "Employed", "Unemployed", "UnemploymentRate"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Clean FIPS codes
    df["StateFIPS"] = df["StateFIPS"].astype(str).str.split(".").str[0].str.zfill(2)
    df["CountyFIPS"] = df["CountyFIPS"].astype(str).str.split(".").str[0].str.zfill(3)
    df["FIPS"] = df["StateFIPS"] + df["CountyFIPS"]

    # Drop missing values and return final data
    df = df.dropna(subset=["UnemploymentRate", "FIPS"])
    bls_final = df[["FIPS", "CountyName", "UnemploymentRate", "LaborForce"]].copy()
    bls_final["FIPS"] = bls_final["FIPS"].astype(str)

    print(f"BLS data loaded: {bls_final.shape[0]} counties")
    return bls_final

def load_census_economic_data():
    """
    Load census economic data including income, population, and poverty.

    Returns:
        pandas.DataFrame: Census economic data with calculated poverty rate
    """
    print("Loading Census economic data...")

    try:
        # Fetch data from Census API
        econ = census_client.acs5.state_county(
            fields=["NAME", "B19013_001E", "B01003_001E", "B17001_002E"],
            state_fips="*",
            county_fips="*",
            year=CENSUS_YEAR,
        )

        # Convert to DataFrame and rename columns
        econ_df = pd.DataFrame(econ)
        econ_df = econ_df.rename(
            columns={
                "NAME": "County_Name",
                "B19013_001E": "Median_Income",
                "B01003_001E": "Population",
                "B17001_002E": "Poverty_Count",
            }
        )

        # Create FIPS code
        econ_df["FIPS"] = (
            econ_df["state"].astype(str).str.zfill(2) +
            econ_df["county"].astype(str).str.zfill(3)
        )

        # Convert to numeric and calculate poverty rate
        econ_df["Median_Income"] = pd.to_numeric(econ_df["Median_Income"], errors="coerce")
        econ_df["Population"] = pd.to_numeric(econ_df["Population"], errors="coerce")
        econ_df["Poverty_Count"] = pd.to_numeric(econ_df["Poverty_Count"], errors="coerce")
        econ_df["Poverty_Rate"] = (econ_df["Poverty_Count"] / econ_df["Population"]) * 100

        # Return selected columns
        return econ_df[["FIPS", "County_Name", "Median_Income", "Population", "Poverty_Rate"]]

    except Exception as e:
        print(f"Error loading economic data: {e}")
        return None

def load_census_education_data():
    """
    Load census education data for bachelor's degree and higher.

    Returns:
        pandas.DataFrame: Census education data with college educated percentage
    """
    print("Loading Census education data...")

    try:
        # Fetch data from Census API
        edu = census_client.acs5.state_county(
            fields=[
                "NAME", "B15003_022E", "B15003_023E", "B15003_024E",
                "B15003_025E", "B15003_001E"
            ],
            state_fips="*",
            county_fips="*",
            year=CENSUS_YEAR,
        )

        # Convert to DataFrame and rename columns
        edu_df = pd.DataFrame(edu)
        edu_df = edu_df.rename(
            columns={
                "NAME": "County_Name",
                "B15003_022E": "Bachelors",
                "B15003_023E": "Masters",
                "B15003_024E": "Professional",
                "B15003_025E": "Doctorate",
                "B15003_001E": "Total_Education",
            }
        )

        # Create FIPS code
        edu_df["FIPS"] = (
            edu_df["state"].astype(str).str.zfill(2) +
            edu_df["county"].astype(str).str.zfill(3)
        )

        # Convert to numeric
        for col in ["Bachelors", "Masters", "Professional", "Doctorate", "Total_Education"]:
            edu_df[col] = pd.to_numeric(edu_df[col], errors="coerce")

        # Calculate college educated percentage
        edu_df["BachelorPlus"] = (
            edu_df["Bachelors"] + edu_df["Masters"] +
            edu_df["Professional"] + edu_df["Doctorate"]
        )
        edu_df["College_Educated_Pct"] = (
            edu_df["BachelorPlus"] / edu_df["Total_Education"] * 100
        )

        # Return selected columns
        return edu_df[[
            "FIPS", "Bachelors", "Masters", "Professional", "Doctorate",
            "Total_Education", "BachelorPlus", "College_Educated_Pct"
        ]]

    except Exception as e:
        print(f"Error loading education data: {e}")
        return None