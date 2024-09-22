import os
import json
import pandas as pd

# List of JSON filenames to process (these should be the new extracted files)
extracted_json_files = [
    "extracted_bars_data_la.json",
    "extracted_bus_stops_data_la.json",
    "extracted_convenience_stores_data_la.json",
    "extracted_gas_stations_data_la.json",
    "extracted_grocery_stores_data_la.json",
    "extracted_la_parks_data.json",
    "extracted_museums_data_la.json",
    "extracted_pawn_shops_data_la.json",
    "extracted_schools_data_la.json",
    "extracted_subway_stations_data_la.json"
]

# Create an Excel writer object
output_excel_path = "extracted_data.xlsx"
with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
    # Process each JSON file and write data to a separate sheet in the Excel file
    for json_file in extracted_json_files:
        # Extract the base name of the file to use as the sheet name (without 'extracted_' prefix)
        sheet_name = os.path.splitext(json_file.replace("extracted_", ""))[0]

        # Load the JSON data
        file_path = os.path.join(os.getcwd(), json_file)
        with open(file_path, 'r') as file:
            nodes = json.load(file)

        # Convert the JSON data to a DataFrame
        df = pd.DataFrame(nodes)

        # Write the DataFrame to a separate sheet in the Excel file
        df.to_excel(writer, index=False, sheet_name=sheet_name, columns=['id', 'lat', 'lon'])

    print(f"Data has been successfully written to {output_excel_path}")
