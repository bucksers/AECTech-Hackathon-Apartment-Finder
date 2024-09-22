import requests
import json

# Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the Overpass query for parks in Los Angeles County
# The bounding box [min_lon, min_lat, max_lon, max_lat] approximately covers Los Angeles County
overpass_query = """
[out:json];
area["name"="Los Angeles County"]["boundary"="administrative"]->.a;
(
  node["leisure"="park"](area.a);
  way["leisure"="park"](area.a);
  relation["leisure"="park"](area.a);
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
    parks_data = response.json()
    
    # Save the parks data to a JSON file
    with open("la_parks_data.json", "w") as json_file:
        json.dump(parks_data, json_file, indent=4)
    
    print("Parks data saved to la_parks_data.json")
    print(f"Number of elements retrieved: {len(parks_data.get('elements', []))}")
else:
    print(f"Failed to retrieve parks data. Status code: {response.status_code}")
    print("Error message:", response.text)

from pprint import pprint

# Load the JSON data from the file
with open("la_parks_data.json", "r") as json_file:
    parks_data = json.load(json_file)

# Use pprint to print the JSON structure in a readable format
pprint(parks_data)