import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

def load_well_data(file_path: str) -> pd.DataFrame:
    """Load and preprocess the well data."""
    df = pd.read_excel(file_path)
    # Add preprocessing steps here (e.g., data type conversion)
    return df

def load_monitoring_data(folder_path: str, well_df: pd.DataFrame) -> pd.DataFrame:
    """Load monitoring data and merge with well data."""
    all_data = []
    for file in os.listdir(folder_path):
        if file.endswith('.xlsx'):
            df = pd.read_excel(os.path.join(folder_path, file))
            merged_data = pd.merge(df, well_df, on='ID')
            all_data.append(merged_data)
    return pd.concat(all_data)

# Load data
well_data = load_well_data('path/to/wells.xlsx')
monitoring_data = load_monitoring_data('path/to/monitoring', well_data)

# Example visualization: Time series plot for a single well
single_well_data = monitoring_data[monitoring_data['ID'] == 'NWP00001']
plt.figure(figsize=(10, 6))
sns.lineplot(data=single_well_data, x='Date and Time', y='Value')
plt.title('Water Depth Over Time for Well NWP00001')
plt.xlabel('Date and Time')
plt.ylabel('Water Depth (m)')
plt.show()
