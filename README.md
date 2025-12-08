# Analysis of Socio-Economic Factors on US Housing Markets at County Level

## Introduction
This project examines how different social and economic factors affect housing prices across counties in the United States. Using publicly available data, the analysis explores connections between home values and key indicators like income, unemployment rates, poverty levels, and education. Statistical methods and clustering techniques are applied to identify patterns, group similar counties, and understand regional differences in housing affordability.
## Data Sources

| # | Data Source | Description | Format | List of Fields | Estimated Data Size |
|---|-------------|-------------|--------|----------------|---------------------|
| 1 | Zillow Home Value Index - County Level | Median home values by county | CSV | RegionName, State, StateCodeFIPS, MunicipalCodeFIPS, 2022-12-31 (median home value) | 3,073 records |
| 2 | U.S. Census Bureau - Socio-economic Data | Median income, population, poverty, education levels | API (JSON) | state, county, B19013_001E (median income), B01003_001E (population), B17001_002E (poverty count), B15003_022E (bachelors), B15003_023E (masters), B15003_024E (professional), B15003_025E (doctorate), B15003_001E (total education) | 3,222 records |
| 3 | Bureau of Labor Statistics - Employment Data | Unemployment rates and labor force data | XLSX | State FIPS, County FIPS, Unemployment Rate, Labor Force | 3,225 records |

## Analysis
The project employs several analytical techniques to examine the relationship between housing prices and socio-economic factors:

1. **Exploratory Data Analysis (EDA)**: Initial examination of data distributions, missing values, and summary statistics for all variables.
2. **Correlation Analysis**: Calculation of correlation coefficients and visualization through correlation matrices and scatter plots to identify statistical relationships between housing prices and socio-economic indicators.
3. **K-means Clustering**: Application of unsupervised learning to group counties with similar characteristics using the elbow method for optimal cluster number selection.
4. **Feature Importance Analysis**: Evaluation of which socio-economic factors have the strongest influence on housing prices through regression analysis and feature ranking.
5. **Comparative Regional Analysis**: Examination of cluster distributions across different states and regions to identify geographic patterns.
6. **Outlier Detection**: Identification and analysis of counties that deviate from expected socio-economic and housing patterns.

## Summary of Results
1. **Income and education are the strongest predictors** of county-level home values among socio-economic factors analyzed.
2. **Clear economic stratification** exists in the US housing market, with analysis revealing four distinct county profiles based on housing and socio-economic characteristics.
3. **Tourist and resort areas represent outliers**, often priced far above what socio-economic fundamentals would predict, following "different rules" in local market pricing.
4. **Regional disparities are evident** in both housing affordability and socio-economic conditions across different geographic areas.

## How to Run
Follow these steps to reproduce the analysis:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
Create a .env file in the project root directory and add your API key:
```bash
CENSUS_API_KEY=your_census_api_key_here
```

To obtain a Census API key:

1. Visit: https://api.census.gov/data/key_signup.html
2. Sign up for a free API key
3. Add the key to your .env file

### 3. Run the Data Pipeline
Execute the main script to fetch and process all data:
```bash
python src/main.py
```

### 4. Execute the Analysis
#### For complete analysis and visualizations, open and run `results.ipynb` in Jupyter Notebook. This notebook contains:

1. Complete exploratory data analysiz
2. Correlation analysis with visualizations
3. K-means clustering implementation and evaluation
4. Feature importance analysis
5. Regional comparative analysis
6. All final visualizations and interpretations

### Additionaly
If you encounter SSL certificate errors when connecting to the data sources, add these lines:
```bash
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

