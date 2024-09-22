import requests
import json

# Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the Overpass query for grocery stores in Los Angeles County
# This query uses the administrative boundary of Los Angeles County.
overpass_query = """
[out:json];
area["name"="Los Angeles County"]["boundary"="administrative"]->.a;
(
  node["shop"="supermarket"](area.a);
  way["shop"="supermarket"](area.a);
  relation["shop"="supermarket"](area.a);
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
    grocery_stores_data = response.json()
    
    # Save the grocery stores data to a JSON file
    with open("grocery_stores_data_la.json", "w") as json_file:
        json.dump(grocery_stores_data, json_file, indent=4)
    
    print("Grocery stores data saved to grocery_stores_data_la.json")
    print(f"Number of elements retrieved: {len(grocery_stores_data.get('elements', []))}")
else:
    print(f"Failed to retrieve grocery stores data. Status code: {response.status_code}")
    print("Error message:", response.text)
