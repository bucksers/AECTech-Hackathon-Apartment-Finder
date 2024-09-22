import requests
import json

# Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the Overpass query for bars in Los Angeles County
# This query uses the administrative boundary of Los Angeles County.
overpass_query = """
[out:json];
area["name"="Los Angeles County"]["boundary"="administrative"]->.a;
(
  node["amenity"="bar"](area.a);
  way["amenity"="bar"](area.a);
  relation["amenity"="bar"](area.a);
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
    bars_data = response.json()
    
    # Save the bars data to a JSON file
    with open("bars_data_la.json", "w") as json_file:
        json.dump(bars_data, json_file, indent=4)
    
    print("Bars data saved to bars_data_la.json")
    print(f"Number of elements retrieved: {len(bars_data.get('elements', []))}")
else:
    print(f"Failed to retrieve bars data. Status code: {response.status_code}")
    print("Error message:", response.text)
