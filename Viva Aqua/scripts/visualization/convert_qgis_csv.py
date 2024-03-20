import csv
filename = "visualization/data/interpolated_groundwater_dataset.csv"
output_filename = "visualization/data/interpolated_groundwater_dataset_cleaned.csv"

# Open the input and output files
with open(filename, 'r') as input_file, open(output_filename, 'w', newline='') as output_file:
    # Create a CSV reader and writer
    reader = csv.reader(input_file, delimiter=';')
    writer = csv.writer(output_file, delimiter=',')

    # Read the header row
    header = next(reader)
    header = header[3:]

    # Rename the column headers
    header[0] = "Groundwater Level (m)"
    header[1] = "Longitude"
    header[2] = "Latitude"

    # Write the modified header to the output file
    writer.writerow(header)

    # Iterate over each row in the input file
    for row in reader:
        # Remove the first 3 columns
        row = row[3:]

        # Convert each value in the row
        converted_row = [value.replace(',', '.') for value in row]

        # Negate the groundwater level
        converted_row[0] = str(-float(converted_row[0]))

        # Write the converted row to the output file
        writer.writerow(converted_row)
