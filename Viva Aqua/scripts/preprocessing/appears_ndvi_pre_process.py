import os
import pandas as pd
from datetime import datetime

def clean_and_save_ndvi_dataset(csv_path: str, output_directory: str) -> None:
    """
    Reads a dataset, filters and cleans it, forward-fills missing dates, 
    and saves the cleaned data in the specified output directory. 

    Parameters:
    csv_path (str): Path to the CSV file.
    output_directory (str): Path to the output directory where the cleaned file will be saved.

    Returns:
    None
    """
    try:
        # Load the dataset
        data = pd.read_csv(csv_path)

        # Perform initial filtering and selection
        specified_value = '0b00000000000000000000000000000000'
        total_rows = len(data)
        specified_value_count = (data['MOD13Q1_061__250m_16_days_pixel_reliability_MODLAND'] == specified_value).sum()
        percentage_with_value = (specified_value_count / total_rows) * 100

        print(f"Percentage of rows with value '{specified_value}': {percentage_with_value:.2f}%")

        filtered_data = data[data['MOD13Q1_061__250m_16_days_pixel_reliability_MODLAND'] == specified_value]

        columns_to_keep = [
            'Latitude', 'Longitude', 'Date', 
            'MOD13Q1_061__250m_16_days_EVI', 
            'MOD13Q1_061__250m_16_days_MIR_reflectance', 
            'MOD13Q1_061__250m_16_days_NDVI'
        ]
        cleaned_data = filtered_data[columns_to_keep]

        print(f"Number of rows after cleaning: {len(cleaned_data)}")

        # Convert 'Date' to datetime and set as index
        cleaned_data.loc[:, 'Date'] = pd.to_datetime(cleaned_data['Date'])
        cleaned_data.set_index('Date', inplace=True)

        # Create a continuous date range from start to end
        date_range = pd.date_range(start=cleaned_data.index.min(), end=cleaned_data.index.max())
        cleaned_data = cleaned_data.reindex(date_range)

        # Forward-fill the missing values
        cleaned_data.ffill(inplace=True)

        # Reset index to add the 'Date' column back
        cleaned_data.reset_index(inplace=True)
        cleaned_data.rename(columns={'index': 'Date'}, inplace=True)

        # Construct the output file path
        filename = os.path.basename(csv_path)
        output_file_path = os.path.join(output_directory, filename)

        # Save the cleaned data to the output file
        cleaned_data.to_csv(output_file_path, index=False)

        # Print final information about the cleaned data
        print(f"Data cleaning complete. Number of rows after cleaning and filling: {len(cleaned_data)}")

    except KeyError as e:
        print(f"KeyError encountered in file {csv_path}: {e}")
        return

# Usage example
# clean_and_save_dataset('path_to_your_file.csv')

def process_all_csv_in_directory(directory_path: str, output_directory: str) -> None:
    """
    Applies the clean_and_save_ndvi_dataset function to all CSV files in the given directory
    and saves the cleaned files in the specified output directory.

    Parameters:
    directory_path (str): Path to the directory containing CSV files.
    output_directory (str): Path to the directory where the cleaned files will be saved.

    Returns:
    None
    """
    # List all files in the directory
    files = os.listdir(directory_path)

    # Loop through the files and apply the function to each CSV file
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(directory_path, file)
            print(f"Processing file: {file_path}")
            clean_and_save_ndvi_dataset(file_path, output_directory)
            print(f"Finished processing: {file_path}")

# Usage example
# process_all_csv_in_directory('path_to_your_directory', 'path_to_your_output_directory')

def merge_additional_data(main_df_path: str, additional_data_dir: str) -> pd.DataFrame:
    """
    Merges additional data into the main dataframe based on ID and Date.

    Parameters:
    main_df_path (str): Path to the main CSV file.
    additional_data_dir (str): Directory containing additional CSV files.

    Returns:
    pd.DataFrame: The main dataframe with additional data merged.
    """
    # Load the main dataframe
    main_df = pd.read_csv(main_df_path)
    main_df['Date'] = pd.to_datetime(main_df['Date'])
    print(f"Initial number of rows in main dataframe: {len(main_df)}")

    merged_dataframes = []  # List to hold merged dataframes

    # Iterate over each file in the additional data directory
    for file in os.listdir(additional_data_dir):
        if file.endswith('.csv'):
            id = file.split('.')[0]  # Extract ID from filename
            additional_df = pd.read_csv(os.path.join(additional_data_dir, file))
            additional_df['Date'] = pd.to_datetime(additional_df['Date'])

            # Filter main_df for rows matching the current ID
            filtered_main_df = main_df[main_df['ID'] == id]

            # Merge the filtered main dataframe with additional data based on 'Date'
            merged_df = pd.merge(filtered_main_df, additional_df, on='Date', how='left')
            merged_dataframes.append(merged_df)

    # Concatenate all merged dataframes
    final_df = pd.concat(merged_dataframes, ignore_index=True)

    # Drop duplicates
    final_df = final_df.drop_duplicates(subset=['ID', 'Date'])

    print(f"Number of rows in final dataframe: {len(final_df)}")
    return final_df

# Usage example
# main_df_path = 'path_to/merged_data_gambia.csv'
# additional_data_dir = 'path_to/data/processed_data/appears/ndvi/'
# merged_df = merge_additional_data(main_df_path, additional_data_dir)