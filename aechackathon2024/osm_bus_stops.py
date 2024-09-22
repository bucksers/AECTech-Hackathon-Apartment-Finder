import requests
import json

# Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the Overpass query for bus stops in Los Angeles County
# This query uses the administrative boundary of Los Angeles County.
overpass_query = """
[out:json];
area["name"="Los Angeles County"]["boundary"="administrative"]->.a;
(
  node["highway"="bus_stop"](area.a);
  way["highway"="bus_stop"](area.a);
  relation["highway"="bus_stop"](area.a);
);
out body;
>;
out skel qt;
"""

# Make the API request
response = requests.get(overpass_url, params={'data': overpass_query})

# Check if the request was successful
if response.status_code == 200:
    # Parse the response as JSON
    bus_stops_data = response.json()
    
    # Save the bus stops data to a JSON file
    with open("bus_stops_data_la.json", "w") as json_file:
        json.dump(bus_stops_data, json_file, indent=4)
    
    print("Bus stops data saved to bus_stops_data_la.json")
    print(f"Number of elements retrieved: {len(bus_stops_data.get('elements', []))}")
else:
    print(f"Failed to retrieve bus stops data. Status code: {response.status_code}")
    print("Error message:", response.text)
