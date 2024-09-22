import requests
import json

# Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define the Overpass query for schools in Los Angeles County
# This query uses the administrative boundary of Los Angeles County.
overpass_query = """
[out:json];
area["name"="Los Angeles County"]["boundary"="administrative"]->.a;
(
  node["amenity"="school"](area.a);
  way["amenity"="school"](area.a);
  relation["amenity"="school"](area.a);
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
    schools_data = response.json()
    
    # Save the schools data to a JSON file
    with open("schools_data_la.json", "w") as json_file:
        json.dump(schools_data, json_file, indent=4)
    
    print("Schools data saved to schools_data_la.json")
    print(f"Number of elements retrieved: {len(schools_data.get('elements', []))}")
else:
    print(f"Failed to retrieve schools data. Status code: {response.status_code}")
    print("Error message:", response.text)
