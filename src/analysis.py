"""
Analysis module for the project.
Functions for statistical analysis and visualizations.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import from config
from config import *

def basic_descriptive_statistics(merged_data):
    """
    Calculate and display basic descriptive statistics.

    Args:
        merged_data: Final merged dataset

    Returns:
        pandas.DataFrame: Descriptive statistics table
    """
    print("BASIC DESCRIPTIVE STATISTICS")

    # Select numeric columns
    numeric_columns = merged_data.select_dtypes(include=[np.number]).columns.tolist()
    stats = merged_data[numeric_columns].describe()

    # Display statistics
    print(stats)

    # Key statistics
    print("KEY STATISTICS")
    print(f"Counties analyzed: {len(merged_data)}")
    print(f"Average home value: ${merged_data['MedianHomeValue'].mean():,.0f}")
    print(f"Average household income: ${merged_data['Median_Income'].mean():,.0f}")
    print(f"Average poverty rate: {merged_data['Poverty_Rate'].mean():.1f}%")
    print(f"Average college educated: {merged_data['College_Educated_Pct'].mean():.1f}%")
    print(f"Average unemployment rate: {merged_data['UnemploymentRate'].mean():.1f}%")

    # Additional statistics
    print(f"Median home value: ${merged_data['MedianHomeValue'].median():,.0f}")
    print(f"Median household income: ${merged_data['Median_Income'].median():,.0f}")
    print(f"Standard deviation of home values: ${merged_data['MedianHomeValue'].std():,.0f}")

    return stats

def correlation_analysis(merged_data):
    """
    Calculate correlations between key variables.

    Args:
        merged_data: Final merged dataset

    Returns:
        pandas.DataFrame: Correlation matrix
    """
    print("CORRELATION ANALYSIS")

    # Select key variables for correlation
    corr_vars = [
        'MedianHomeValue', 'Median_Income', 'Poverty_Rate',
        'College_Educated_Pct', 'UnemploymentRate'
    ]

    # Calculate correlation matrix
    correlation_matrix = merged_data[corr_vars].corr()

    print("Correlation matrix:")
    print(correlation_matrix)

    # Print strongest correlations
    print("Top correlations with Median Home Value:")
    home_value_corr = correlation_matrix['MedianHomeValue'].sort_values(ascending=False)
    for var, corr in home_value_corr.items():
        if var != 'MedianHomeValue':
            print(f"{var}: {corr:.3f}")

    return correlation_matrix

def create_visualizations(merged_data):
    """
    Create visualizations for the analysis.

    Args:
        merged_data: Final merged dataset
    """
    print("CREATING VISUALIZATIONS")

    # Set up the figure
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('US County-Level Analysis', fontsize=16)

    # 1. Histogram of home values
    axes[0, 0].hist(merged_data['MedianHomeValue'], bins=50, edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('Distribution of Home Values')
    axes[0, 0].set_xlabel('Median Home Value ($)')
    axes[0, 0].set_ylabel('Number of Counties')
    axes[0, 0].ticklabel_format(style='plain', axis='x')

    # 2. Scatter plot: Home Value vs Income
    axes[0, 1].scatter(merged_data['Median_Income'], merged_data['MedianHomeValue'],
                       alpha=0.5, s=10)
    axes[0, 1].set_title('Home Value vs Household Income')
    axes[0, 1].set_xlabel('Median Household Income ($)')
    axes[0, 1].set_ylabel('Median Home Value ($)')

    # 3. Scatter plot: Home Value vs Education
    axes[0, 2].scatter(merged_data['College_Educated_Pct'], merged_data['MedianHomeValue'],
                       alpha=0.5, s=10)
    axes[0, 2].set_title('Home Value vs College Education')
    axes[0, 2].set_xlabel('College Educated (%)')
    axes[0, 2].set_ylabel('Median Home Value ($)')

    # 4. Scatter plot: Home Value vs Poverty
    axes[1, 0].scatter(merged_data['Poverty_Rate'], merged_data['MedianHomeValue'],
                       alpha=0.5, s=10)
    axes[1, 0].set_title('Home Value vs Poverty Rate')
    axes[1, 0].set_xlabel('Poverty Rate (%)')
    axes[1, 0].set_ylabel('Median Home Value ($)')

    # 5. Scatter plot: Home Value vs Unemployment
    axes[1, 1].scatter(merged_data['UnemploymentRate'], merged_data['MedianHomeValue'],
                       alpha=0.5, s=10)
    axes[1, 1].set_title('Home Value vs Unemployment')
    axes[1, 1].set_xlabel('Unemployment Rate (%)')
    axes[1, 1].set_ylabel('Median Home Value ($)')

    # 6. Bar chart: Top 10 counties by home value
    top_counties = merged_data.nlargest(10, 'MedianHomeValue')
    axes[1, 2].barh(range(len(top_counties)), top_counties['MedianHomeValue'])
    axes[1, 2].set_yticks(range(len(top_counties)))
    axes[1, 2].set_yticklabels(top_counties['County'], fontsize=8)
    axes[1, 2].set_title('Top 10 Counties by Home Value')
    axes[1, 2].set_xlabel('Median Home Value ($)')

    plt.tight_layout()
    plt.savefig('county_analysis_visualizations.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("Visualizations saved to 'county_analysis_visualizations.png'")

    # Create correlation heatmap
    plt.figure(figsize=(10, 8))
    corr_matrix = correlation_analysis(merged_data)
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": .8})
    plt.title('Correlation Matrix of Key Variables')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("Correlation matrix saved to 'correlation_matrix.png'")

def state_level_analysis(merged_data):
    """
    Perform analysis at state level.

    Args:
        merged_data: Final merged dataset

    Returns:
        pandas.DataFrame: State-level aggregated statistics
    """
    print("STATE-LEVEL ANALYSIS")

    # Group by state and calculate averages
    state_stats = merged_data.groupby('State').agg({
        'MedianHomeValue': 'mean',
        'Median_Income': 'mean',
        'Poverty_Rate': 'mean',
        'College_Educated_Pct': 'mean',
        'UnemploymentRate': 'mean',
        'FIPS': 'count'  # Number of counties
    }).rename(columns={'FIPS': 'CountyCount'})

    state_stats = state_stats.sort_values('MedianHomeValue', ascending=False)

    print("Top 10 states by average home value:")
    print(state_stats[['MedianHomeValue', 'CountyCount']].head(10))

    print("Bottom 10 states by average home value:")
    print(state_stats[['MedianHomeValue', 'CountyCount']].tail(10))

    # Create state-level visualization
    plt.figure(figsize=(12, 6))
    top_states = state_stats.nlargest(15, 'MedianHomeValue')
    plt.bar(range(len(top_states)), top_states['MedianHomeValue'])
    plt.xticks(range(len(top_states)), top_states.index, rotation=45, ha='right')
    plt.ylabel('Average Median Home Value ($)')
    plt.title('Top 15 States by Average Home Value')
    plt.tight_layout()
    plt.savefig('state_level_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("State-level analysis saved to 'state_level_analysis.png'")

    return state_stats

def save_analysis_results(merged_data, stats, correlation_matrix, state_stats):
    """
    Save all analysis results to files.

    Args:
        merged_data: Final merged dataset
        stats: Descriptive statistics
        correlation_matrix: Correlation matrix
        state_stats: State-level statistics
    """
    print("SAVING ANALYSIS RESULTS")

    # Save merged data
    merged_data.to_csv('final_merged_data.csv', index=False)
    print("Final dataset saved to 'final_merged_data.csv'")

    # Save descriptive statistics
    stats.to_csv('descriptive_statistics.csv')
    print("Descriptive statistics saved to 'descriptive_statistics.csv'")

    # Save correlation matrix
    correlation_matrix.to_csv('correlation_matrix.csv')
    print("Correlation matrix saved to 'correlation_matrix.csv'")

    # Save state statistics
    state_stats.to_csv('state_level_statistics.csv')
    print("State-level statistics saved to 'state_level_statistics.csv'")

    # Create summary report
    with open('analysis_summary.txt', 'w') as f:
        f.write("ANALYSIS SUMMARY REPORT\n")
        f.write("="*50 + "\n\n")
        f.write(f"Total counties analyzed: {len(merged_data)}\n")
        f.write(f"Average home value: ${merged_data['MedianHomeValue'].mean():,.0f}\n")
        f.write(f"Average household income: ${merged_data['Median_Income'].mean():,.0f}\n")
        f.write(f"Average poverty rate: {merged_data['Poverty_Rate'].mean():.1f}%\n")
        f.write(f"Average college educated: {merged_data['College_Educated_Pct'].mean():.1f}%\n")
        f.write(f"Average unemployment rate: {merged_data['UnemploymentRate'].mean():.1f}%\n\n")

        f.write("TOP CORRELATIONS WITH HOME VALUE:\n")
        home_value_corr = correlation_matrix['MedianHomeValue'].sort_values(ascending=False)
        for var, corr in home_value_corr.items():
            if var != 'MedianHomeValue':
                f.write(f"{var}: {corr:.3f}\n")

    print("Analysis summary saved to 'analysis_summary.txt'")
    print("Analysis complete. Check generated files for results.")

def run_analysis(merged_data):
    """
    Run complete analysis pipeline.

    Args:
        merged_data: Final merged dataset

    Returns:
        dict: Dictionary containing all analysis results
    """
    if merged_data is None:
        print("No data provided for analysis")
        return

    print("STARTING ANALYSIS")

    # Run all analysis functions
    stats = basic_descriptive_statistics(merged_data)
    correlation_matrix = correlation_analysis(merged_data)
    create_visualizations(merged_data)
    state_stats = state_level_analysis(merged_data)
    save_analysis_results(merged_data, stats, correlation_matrix, state_stats)

    return {
        'stats': stats,
        'correlation_matrix': correlation_matrix,
        'state_stats': state_stats
    }