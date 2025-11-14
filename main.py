import pandas as pd
import requests
from census import Census
import ssl
from config import CENSUS_API_KEY

ssl._create_default_https_context = ssl._create_unverified_context

c = Census(CENSUS_API_KEY)
def show_zillow_data_sample():

    try:
        zillow_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
        zillow_df = pd.read_csv(zillow_url)

        print(f"Data size: {zillow_df.shape}")
        print(f"Columns: {list(zillow_df.columns[:10])}...")  # Show first 10 columns

        # Show main columns
        display_columns = ['RegionName', 'State', 'StateName', 'SizeRank']
        # Add latest date (price)
        date_columns = [col for col in zillow_df.columns if col.startswith('20')]
        if date_columns:
            latest_date = date_columns[-1]
            display_columns.append(latest_date)

        print("\nFirst 10 rows:")
        print(zillow_df[display_columns].head(10))

        print(f"\nTotal counties: {len(zillow_df)}")
        return zillow_df

    except Exception as e:
        print(f"Error loading Zillow data: {e}")
        return None


def show_census_economic_data_sample():
    """Show sample Census economic data"""
    print("\n" + "=" * 50)
    print("CENSUS ECONOMIC DATA")
    print("=" * 50)

    try:
        census_data = c.acs5.state_county(
            fields=['NAME', 'B19013_001E', 'B01003_001E', 'B17001_002E'],
            state_fips='*',
            county_fips='*',
            year=2022
        )

        econ_df = pd.DataFrame(census_data)

        print(f"Data size: {econ_df.shape}")
        print(f"Columns: {list(econ_df.columns)}")

        # Rename for clarity
        econ_display = econ_df.rename(columns={
            'NAME': 'County_Name',
            'B19013_001E': 'Median_Income',
            'B01003_001E': 'Population',
            'B17001_002E': 'Poverty_Count'
        })

        print("\nFirst 10 rows:")
        print(econ_display[['County_Name', 'state', 'county', 'Median_Income', 'Population']].head(10))

        print(f"\nTotal counties: {len(econ_df)}")
        return econ_df

    except Exception as e:
        print(f"Error loading economic data: {e}")
        return None


def show_census_education_data_sample():
    """Show sample Census education data"""
    print("\n" + "=" * 50)
    print("CENSUS EDUCATION DATA")
    print("=" * 50)

    try:
        education_data = c.acs5.state_county(
            fields=['NAME', 'B15003_022E', 'B15003_023E', 'B15003_024E', 'B15003_025E', 'B15003_001E'],
            state_fips='*',
            county_fips='*',
            year=2022
        )

        edu_df = pd.DataFrame(education_data)

        print(f"Data size: {edu_df.shape}")
        print(f"Columns: {list(edu_df.columns)}")

        # Rename for clarity
        edu_display = edu_df.rename(columns={
            'NAME': 'County_Name',
            'B15003_022E': 'Bachelors',
            'B15003_023E': 'Masters',
            'B15003_024E': 'Professional',
            'B15003_025E': 'Doctorate',
            'B15003_001E': 'Total_Education'
        })

        print("\nFirst 10 rows:")
        print(edu_display[['County_Name', 'state', 'county', 'Bachelors', 'Masters', 'Total_Education']].head(10))

        print(f"\nTotal counties: {len(edu_df)}")
        return edu_df

    except Exception as e:
        print(f"Error loading education data: {e}")
        return None


def show_merged_sample():
    """Show sample merged data"""
    print("\n" + "=" * 50)
    print("MERGED DATA")
    print("=" * 50)

    # Get all data
    zillow_data = show_zillow_data_sample()
    economic_data = show_census_economic_data_sample()
    education_data = show_census_education_data_sample()

    if zillow_data is not None and economic_data is not None and education_data is not None:
        try:
            # Prepare Zillow data
            date_columns = [col for col in zillow_data.columns if col.startswith('20')]
            latest_date = date_columns[-1] if date_columns else None

            zillow_clean = zillow_data[['RegionName', 'State', latest_date]].copy()
            zillow_clean.columns = ['County', 'State', 'MedianHomeValue']

            # Create FIPS code for Zillow
            if 'StateCodeFIPS' in zillow_data.columns and 'MunicipalCodeFIPS' in zillow_data.columns:
                zillow_clean['FIPS'] = zillow_data['StateCodeFIPS'].astype(str).str.zfill(2) + zillow_data[
                    'MunicipalCodeFIPS'].astype(str).str.zfill(3)
                zillow_clean['FIPS'] = zillow_clean['FIPS'].astype(int)
            else:
                zillow_clean['FIPS'] = zillow_data['RegionID']

            # Prepare economic data
            economic_clean = economic_data.copy()
            economic_clean['FIPS'] = economic_clean['state'].astype(str).str.zfill(2) + economic_clean['county'].astype(
                str).str.zfill(3)
            economic_clean['FIPS'] = economic_clean['FIPS'].astype(int)
            economic_clean['MedianHouseholdIncome'] = pd.to_numeric(economic_clean['B19013_001E'], errors='coerce')
            economic_clean['Population'] = pd.to_numeric(economic_clean['B01003_001E'], errors='coerce')

            # Prepare education data
            education_clean = education_data.copy()
            education_clean['FIPS'] = education_clean['state'].astype(str).str.zfill(2) + education_clean[
                'county'].astype(str).str.zfill(3)
            education_clean['FIPS'] = education_clean['FIPS'].astype(int)

            # Calculate percentage with higher education
            for col in ['B15003_022E', 'B15003_023E', 'B15003_024E', 'B15003_025E', 'B15003_001E']:
                education_clean[col] = pd.to_numeric(education_clean[col], errors='coerce')

            education_clean['BachelorPlus'] = (
                    education_clean['B15003_022E'] +
                    education_clean['B15003_023E'] +
                    education_clean['B15003_024E'] +
                    education_clean['B15003_025E']
            )
            education_clean['PercentBachelorPlus'] = (education_clean['BachelorPlus'] / education_clean[
                'B15003_001E']) * 100

            # Merge data
            merged = pd.merge(zillow_clean, economic_clean, on='FIPS', how='inner')
            merged = pd.merge(merged, education_clean, on='FIPS', how='inner')

            # Select final columns
            final_columns = [
                'FIPS', 'County', 'State', 'MedianHomeValue',
                'MedianHouseholdIncome', 'Population', 'PercentBachelorPlus'
            ]

            final_data = merged[final_columns].copy()
            final_data = final_data.dropna()

            print(f"Merged data size: {final_data.shape}")
            print(f"Columns: {list(final_data.columns)}")
            print("\nFirst 10 rows of merged data:")
            print(final_data.head(10))

            # Basic statistics
            print("\nBasic statistics of merged data:")
            print(final_data.describe())

            return final_data

        except Exception as e:
            print(f"Error merging data: {e}")
            return None

    else:
        print("Failed to load all datasets for merging")
        return None