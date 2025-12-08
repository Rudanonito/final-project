"""
Configuration file for the project.
Contains all constants, URLs, and settings used throughout the project.
"""

# Data URLs
ZILLOW_URL = "https://files.zillowstatic.com/research/public_csvs/zhvi/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
BLS_FILE_ID = "190XVquIr4BWg97RKJY5fmFSHN6Xf7a_m"
BLS_DATA_URL = f"https://docs.google.com/spreadsheets/d/{BLS_FILE_ID}/export?format=csv"

# Data processing parameters
CENSUS_YEAR = 2022
LATEST_DATE = "2022-12-31"

# Visualization settings
PLOT_STYLE = "default"
SEABORN_PALETTE = "husl"
PD_DISPLAY_MAX_COLUMNS = 50

# Environment variable names
CENSUS_API_KEY_VAR = "CENSUS_API_KEY"