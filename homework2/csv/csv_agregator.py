import re

import pandas as pd
import os


if __name__ == '__main__':
    # Directory containing the CSV files
    directory = "./min_max_alpha_beta_pruning_hr_vs_normal_games"  # Replace with your directory path


    # Function to extract the number from the filename
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group()) if match else 0


    # Get a list of all relevant CSV files and sort them by number
    csv_files = [file for file in os.listdir(directory) if file.startswith("games_") and file.endswith(".csv")]
    csv_files.sort(key=extract_number)

    # Initialize an empty DataFrame to store concatenated data
    concatenated_df = pd.DataFrame()

    # Iterate over the sorted list of files
    for file in csv_files:
        # Read the CSV file
        df = pd.read_csv(os.path.join(directory, file))
        # Append the data to the concatenated DataFrame
        concatenated_df = pd.concat([concatenated_df, df])

    # Save the concatenated DataFrame to a new CSV file
    concatenated_df.to_csv("./min_max_alpha_beta_pruning_hr_vs_normal_games/result.csv", index=False)

