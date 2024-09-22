import requests
import json

# Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the Overpass query for museums in Los Angeles County
# This query uses a bounding box around Los Angeles County. Adjust the coordinates if needed.
overpass_query = """
[out:json];
area["name"="Los Angeles County"]["boundary"="administrative"]->.a;
(
  node["tourism"="museum"](area.a);
  way["tourism"="museum"](area.a);
  relation["tourism"="museum"](area.a);
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
    museums_data = response.json()
    
    # Save the museums data to a JSON file
    with open("museums_data_la.json", "w") as json_file:
        json.dump(museums_data, json_file, indent=4)
    
    print("Museums data saved to museums_data_la.json")
    print(f"Number of elements retrieved: {len(museums_data.get('elements', []))}")
else:
    print(f"Failed to retrieve museums data. Status code: {response.status_code}")
    print("Error message:", response.text)
