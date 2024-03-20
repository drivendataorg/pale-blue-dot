import pandas as pd
import matplotlib.pyplot as plt
import climateservaccess as ca

# Define some parameters
LIS_soil_moisture_datatypes = [
    664, 665, 666, 667
]
start_date = '01/01/2015'
end_date = '12/31/2022'
LIS_res = 0.01 # ~1 km resolution
REGION = 'gambia'

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
column_names = [ca.datatypeDict[type_num] for type_num in LIS_soil_moisture_datatypes]
column_names.insert(0, 'Date')
print(column_names)
LIS_df = pd.DataFrame(columns=column_names)

# Read well data
wells_df = pd.read_csv(f'data/processed_data/igrac/wells_{REGION}.csv')

# Get precipitation average for each well
for index, row in wells_df.iterrows():
    
    print(f"\n------ Fetching data for well {row['ID']} ------")

    # Loop through each datatype
    for type_num in LIS_soil_moisture_datatypes:

        # getBox(lat: float, lon: float, res: float)
        df = ca.getDataFrame(type_num, start_date, end_date, "Average", ca.getBox(lat=row['Latitude'], lon=row['Longitude'], res=LIS_res))

        temp_data = pd.DataFrame(df['datatype'].to_list())
            
        # Find all unique values in the column and convert to list
        datatype = check_list('datatype')
        operationtype = check_list('operationtype')
        intervaltype = check_list('intervaltype')

        # Create a dictionary with key as column name and values as list of unique values in the column
        params = {'datatype': datatype, 'operationtype': operationtype, 'intervaltype': intervaltype}

        # Select data from df
        temp_data = pd.DataFrame(df['data'].to_list())

        # Find extreme negative values and replace with NaN
        temp_data['raw_value'] = temp_data['raw_value'].apply(lambda x: float(x) if float(x) > -100 else None)
            
        # Convert date column to datetime
        temp_data['date'] = pd.to_datetime(temp_data['date'])
        
        # Print stats on raw_value
        print(f"NaN values in raw_value: {temp_data['raw_value'].isna().sum()}")
        print(f"Min value in raw_value: {temp_data['raw_value'].min():.3f}")
        print(f"Max value in raw_value: {temp_data['raw_value'].max():.3f}")

        # Save data to df, matching 
        LIS_df['Date'] = temp_data['date']
        LIS_df[ca.datatypeDict[type_num]] = temp_data['raw_value']

    # # Create new column for a weighted average of all datatypes
    # weights = [0.05, 0.15, 0.3, 0.5] # weights for each datatype

    # LIS_df['LIS_Soil_Moisture_Combined'] = 0
    # for i in range(len(LIS_soil_moisture_datatypes)):
    #     LIS_df['LIS_Soil_Moisture_Combined'] += LIS_df[ca.datatypeDict[LIS_soil_moisture_datatypes[i]]] * weights[i]

    # Plot all columns of soil moisture data vs time
    plt.figure(figsize=(20, 10))
    plt.xlabel('Date')
    plt.ylabel('Soil Moisture (m3/m3)')

    for col in LIS_df.columns:
        if col != 'Date':
            plt.plot(LIS_df['Date'], LIS_df[col], label=col)
    plt.legend()
    plt.savefig(f"../../data/original_data/climateserv/lis_soil_moisture/gambia/{row['ID']}.png")

    # Save data to csv
    LIS_df.to_csv(f"../../data/original_data/climateserv/lis_soil_moisture/gambia/{row['ID']}.csv", index=False)