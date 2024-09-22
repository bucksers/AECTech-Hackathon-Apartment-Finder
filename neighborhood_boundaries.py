import requests
import csv

def get_la_neighborhood_boundaries():
    """
    Query the Overpass API to get neighborhood boundaries for Los Angeles.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Overpass query to retrieve boundaries with admin_level=10 (neighborhood level) in Los Angeles
    overpass_query = """
    [out:json];
    area["name"="Los Angeles"]->.la;
    (
      relation["boundary"="administrative"]["admin_level"="10"](area.la);
    );
    out geom;
    """
    
    # Send the request
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code == 200:
        return response.json()  # Return the data in JSON format
    else:
        print(f"Error: {response.status_code}")
        return None

def process_neighborhood_boundaries(neighborhood_boundaries):
    """
    Process the neighborhood boundary data returned from Overpass API.
    Extract neighborhood names and bounding boxes, and store them in a dictionary.
    """
    neighborhood_dict = {}
    
    for element in neighborhood_boundaries['elements']:
        if element['type'] == 'relation' and 'tags' in element and 'name' in element['tags']:
            name = element['tags']['name']
            bbox = element['bounds'] if 'bounds' in element else None
            
            if bbox:
                # Store the bounding box (lat/lon coordinates) in the dictionary with the neighborhood name as key
                neighborhood_dict[name] = {
                    'min_lat': bbox['minlat'],
                    'min_lon': bbox['minlon'],
                    'max_lat': bbox['maxlat'],
                    'max_lon': bbox['maxlon']
                }
    
    return neighborhood_dict

def write_neighborhoods_to_csv(neighborhood_dict, filename='la_neighborhoods.csv'):
    """
    Write the neighborhood names and their corresponding latitude/longitude boundaries to a CSV file.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(["Neighborhood", "Min Latitude", "Min Longitude", "Max Latitude", "Max Longitude"])
        
        # Write the neighborhood data
        for neighborhood, bbox in neighborhood_dict.items():
            writer.writerow([neighborhood, bbox['min_lat'], bbox['min_lon'], bbox['max_lat'], bbox['max_lon']])

# Step 1: Get the neighborhood boundaries from OpenStreetMap via Overpass API
neighborhood_boundaries = get_la_neighborhood_boundaries()

# Step 2: Process the boundaries and store them in a dictionary
if neighborhood_boundaries:
    neighborhood_dict = process_neighborhood_boundaries(neighborhood_boundaries)

    # Step 3: Write the neighborhood data to a CSV file
    write_neighborhoods_to_csv(neighborhood_dict)

    print("Neighborhood boundaries written to la_neighborhoods.csv")
