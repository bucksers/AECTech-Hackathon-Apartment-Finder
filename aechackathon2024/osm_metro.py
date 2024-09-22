import requests
import json

# Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the Overpass query for subway stations in Los Angeles County
# This query uses the administrative boundary of Los Angeles County.
overpass_query = """
[out:json];
area["name"="Los Angeles County"]["boundary"="administrative"]->.a;
(
  node["railway"="station"]["station"="subway"](area.a);
  way["railway"="station"]["station"="subway"](area.a);
  relation["railway"="station"]["station"="subway"](area.a);
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
    subway_stations_data = response.json()
    
    # Save the subway stations data to a JSON file
    with open("subway_stations_data_la.json", "w") as json_file:
        json.dump(subway_stations_data, json_file, indent=4)
    
    print("Subway stations data saved to subway_stations_data_la.json")
    print(f"Number of elements retrieved: {len(subway_stations_data.get('elements', []))}")
else:
    print(f"Failed to retrieve subway stations data. Status code: {response.status_code}")
    print("Error message:", response.text)
