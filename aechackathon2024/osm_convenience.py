import requests
import json

# Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the Overpass query for convenience stores in Los Angeles County
# This query uses the administrative boundary of Los Angeles County.
overpass_query = """
[out:json];
area["name"="Los Angeles County"]["boundary"="administrative"]->.a;
(
  node["shop"="convenience"](area.a);
  way["shop"="convenience"](area.a);
  relation["shop"="convenience"](area.a);
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
    convenience_stores_data = response.json()
    
    # Save the convenience stores data to a JSON file
    with open("convenience_stores_data_la.json", "w") as json_file:
        json.dump(convenience_stores_data, json_file, indent=4)
    
    print("Convenience stores data saved to convenience_stores_data_la.json")
    print(f"Number of elements retrieved: {len(convenience_stores_data.get('elements', []))}")
else:
    print(f"Failed to retrieve convenience stores data. Status code: {response.status_code}")
    print("Error message:", response.text)
