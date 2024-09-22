import requests
import json

# Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the Overpass query for pawn shops in Los Angeles County
# This query uses the administrative boundary of Los Angeles County.
overpass_query = """
[out:json];
area["name"="Los Angeles County"]["boundary"="administrative"]->.a;
(
  node["shop"="pawnbroker"](area.a);
  way["shop"="pawnbroker"](area.a);
  relation["shop"="pawnbroker"](area.a);
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
    pawn_shops_data = response.json()
    
    # Save the pawn shops data to a JSON file
    with open("pawn_shops_data_la.json", "w") as json_file:
        json.dump(pawn_shops_data, json_file, indent=4)
    
    print("Pawn shops data saved to pawn_shops_data_la.json")
    print(f"Number of elements retrieved: {len(pawn_shops_data.get('elements', []))}")
else:
    print(f"Failed to retrieve pawn shops data. Status code: {response.status_code}")
    print("Error message:", response.text)
