import requests
import pandas as pd
from main import *

# Main function
if __name__ == "__main__":

    # Load and display all data
    final_data = show_merged_sample()

    if final_data is not None:
        print(f"\nSuccessfully loaded data for {len(final_data)} counties")
    else:
        print("\nFailed to load merged data")