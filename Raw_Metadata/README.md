This directory contains the raw metadata collected when running LAMMPS at various number of processes. The raw data is collected in ```.txt``` format.

## Conversion of above text file to csv files
CSV files are mostly used for PCA or data analysis, hence these files are coverted into ``.csv`` files using the below python script:

```python
import csv

# Function to parse the input text and extract relevant information
def parse_text_data(text_data):
    rows = []
    current_row = {}

    for line in text_data.split('\n'):
        line = line.strip()
        if not line:
            continue

        # Check if the line contains ": "
        if ": " not in line:
            continue

        # Split the line into key and value
        key, value = line.split(": ", 1)

        if key == "metadata":
            metadata_parts = value.split(",")
            current_row = {"Name": metadata_parts[0].strip(), "Shape": metadata_parts[1].strip(),
                           "Start": metadata_parts[2].strip(), "Count": metadata_parts[3].strip(),
                           "Constant Shape": metadata_parts[4].strip(), "Time": metadata_parts[5].strip(),
                           "Selection Size": metadata_parts[6].strip(), "SizeofVariable": metadata_parts[7].strip(),
                           "ShapeID": metadata_parts[8].strip(), "Steps": metadata_parts[9].strip(),
                           "StepStart": metadata_parts[10].strip(), "BlockID": metadata_parts[11].strip()}
        elif key == "order":
            order_parts = value.split(": ")
            current_row["OrderKey"] = order_parts[1].strip()
            current_row["OrderOrder"] = order_parts[2].strip()
            rows.append(current_row)

    return rows


# Function to write data to CSV
def write_to_csv(data, csv_filename):
    fieldnames = ["Name", "Shape", "Start", "Count", "Constant Shape", "Time", "Selection Size",
                  "SizeofVariable", "ShapeID", "Steps", "StepStart", "BlockID", "OrderKey", "OrderOrder"]

    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Read data from the text file
with open('32_procs.txt', 'r') as file:
    text_data = file.read()

# Parse the text data
parsed_data = parse_text_data(text_data)

# Write the parsed data to a CSV file
write_to_csv(parsed_data, '32procs.csv')

print("CSV file has been created successfully.")
```
