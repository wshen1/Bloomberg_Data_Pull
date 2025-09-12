import pandas as pd
import os

# --- GLOBAL PROJECT PATHS ---
# This should be the path to the root of your shared project folder.
# NOTE TO STUDENTS: You will likely need to change this path to match
# where you have mounted the shared drive on your local computer.
ROOT_PATH = "/path/to/shared/drive/MMF1941_FALL_2025/"
DATA_LIBRARY_PATH = os.path.join(ROOT_PATH, "01_shared_data_library")

def load_data_from_library(team_folder: str, file_name: str, date_col: str = 'Date') -> pd.DataFrame:
    """
    A general-purpose function to load any CSV file from the shared data library.

    Args:
        team_folder (str): The name of the team folder (e.g., '02_asset_pricing_factors').
        file_name (str): The exact name of the CSV file to load.
        date_col (str): The name of the column to be used as the DataFrame index.

    Returns:
        pd.DataFrame: A pandas DataFrame with a parsed DatetimeIndex, or None if the file is not found.
    """
    # Construct a flexible file path.
    # We will search in both 'raw_data/daily' and 'raw_data/quarterly' for convenience.
    possible_paths = [
        os.path.join(DATA_LIBRARY_PATH, team_folder, "raw_data", "daily", file_name),
        os.path.join(DATA_LIBRARY_PATH, team_folder, "raw_data", "quarterly", file_name),
        os.path.join(DATA_LIBRARY_PATH, team_folder, "processed_data", file_name)
    ]

    file_path_found = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path_found = path
            break

    if not file_path_found:
        print(f"ERROR: File '{file_name}' not found in standard directories for team '{team_folder}'.")
        return None

    print(f"Loading data from: {file_path_found}")
    try:
        # Load the CSV, parsing the specified date column as the index
        df = pd.read_csv(file_path_found, index_col=date_col, parse_dates=True)
        print("File loaded successfully.")
        return df
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return None

# --- Example Usage ---
if __name__ == '__main__':
    # This block will only run when you execute this script directly.
    # It serves as a test and an example for students.
    
    print("\n--- Example: Loading Daily Equity Prices ---")
    # To test this, you would need to create a dummy file at the specified path.
    # For example: MMF1941_FALL_2025/01_shared_data_library/02_asset_pricing_factors/raw_data/daily/sp500_pricing_daily_2005_2025.csv
    
    # daily_prices_df = load_data_from_library(
    #     team_folder="02_asset_pricing_factors",
    #     file_name="sp500_pricing_daily_2005_2025.csv",
    #     date_col='date'
    # )
    
    # if daily_prices_df is not None:
    #     print("Successfully loaded daily prices DataFrame:")
    #     print(daily_prices_df.head())

