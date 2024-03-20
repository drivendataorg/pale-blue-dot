import pandas as pd
import climateservaccess as ca
import time

# Define some parameters
climateserv_datatypes = [
    1
]
start_date = '01/01/2015'
end_date = '12/31/2022'
res = 0.1
REGION = 'gambia'
FOLDER = ca.datatypeDict[climateserv_datatypes[0]]

# Calculate time taken to run script
start_time = time.time()

def check_list(type_name): # check if the list is empty, has one value or multiple values
    type_list = df[type_name].unique().tolist()
    if len(type_list) == 0:
        return None
    elif len(type_list) == 1:
        return float(type_list[0])
    else:
        print(f"Multiple {type_name} found: {type_list}")
        return type_list

# Create a dataframe to store data for all datatypes: a "Date" column and columns for each datatype
column_names = [ca.datatypeDict[type_num] for type_num in climateserv_datatypes]
column_names.insert(0, 'Date')
print(column_names)
output_df = pd.DataFrame(columns=column_names)

# Read well data
wells_df = pd.read_csv(f'data/processed_data/igrac/wells_{REGION}.csv')

# Get precipitation average for each well
for index, row in wells_df.iterrows():
    
    print(f"\n------ Fetching data for well {row['ID']} ------")
    
    # Loop through each datatype
    for type_num in climateserv_datatypes:

        # getBox(lat: float, lon: float, res: float)
        df = ca.getCSV(type_num, start_date, end_date, "Average", ca.getBox(lat=row['Latitude'], lon=row['Longitude'], res=res), f"data/original_data/climateserv/{FOLDER}/{REGION}/{row['ID']}.csv")

# Calculate time taken to run script
end_time = time.time()
print(f"Time taken to run script: {end_time - start_time:.2f} seconds")