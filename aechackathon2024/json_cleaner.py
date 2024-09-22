import os
import json

# List of JSON filenames to process
json_files = [
    "bars_data_la.json",
    "bus_stops_data_la.json",
    "convenience_stores_data_la.json",
    "gas_stations_data_la.json",
    "grocery_stores_data_la.json",
    "la_parks_data.json",
    "museums_data_la.json",
    "pawn_shops_data_la.json",
    "schools_data_la.json",
    "subway_stations_data_la.json"
]

# Function to extract node elements with id, lat, and lon
def extract_nodes(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        nodes = []
        for element in data.get('elements', []):
            if element['type'] == 'node':
                nodes.append({
                    'id': element['id'],
                    'lat': element['lat'],
                    'lon': element['lon']
                })
        return nodes

# Process each JSON file and save the extracted nodes to a new file
for json_file in json_files:
    file_path = os.path.join(os.getcwd(), json_file)
    nodes = extract_nodes(file_path)
    
    # Define the new filename for the extracted nodes
    new_file_name = f"extracted_{json_file}"
    new_file_path = os.path.join(os.getcwd(), new_file_name)
    
    # Save the extracted nodes to the new JSON file
    with open(new_file_path, 'w') as new_file:
        json.dump(nodes, new_file, indent=4)
    
    print(f"Extracted nodes saved to {new_file_name}")
