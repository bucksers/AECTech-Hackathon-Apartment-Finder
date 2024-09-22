import requests
import csv

def get_la_zipcode_boundaries():
    """
    Query the Overpass API to get ZIP code data (via addr:postcode tags) for Los Angeles.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Overpass query to retrieve elements with addr:postcode tag in Los Angeles
    overpass_query = """
    [out:json];
    area["name"="Los Angeles"]->.la;
    (
      node["addr:postcode"](area.la);
      way["addr:postcode"](area.la);
      relation["addr:postcode"](area.la);
    );
    out center;
    """
    
    # Send the request
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code == 200:
        return response.json()  # Return the data in JSON format
    else:
        print(f"Error: {response.status_code}")
        return None

def process_zipcode_boundaries(zipcode_boundaries):
    """
    Process the ZIP code boundary data returned from Overpass API.
    Extract postal codes and their lat/lon centers.
    """
    zipcode_dict = {}
    
    for element in zipcode_boundaries['elements']:
        if 'tags' in element and 'addr:postcode' in element['tags']:
            postal_code = element['tags']['addr:postcode']
            lat = element.get('lat', element.get('center', {}).get('lat'))
            lon = element.get('lon', element.get('center', {}).get('lon'))
            
            if postal_code and lat and lon:
                if postal_code not in zipcode_dict:
                    zipcode_dict[postal_code] = {
                        'postal_code': postal_code,
                        'lat': lat,
                        'lon': lon
                    }
    
    return zipcode_dict

def write_zipcodes_to_csv(zipcode_dict, filename='la_zipcodes.csv'):
    """
    Write the ZIP code center data (lat/lon) to a CSV file.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(["Postal Code", "Latitude", "Longitude"])
        
        # Write the ZIP code data
        for postal_code, data in zipcode_dict.items():
            writer.writerow([data['postal_code'], data['lat'], data['lon']])

# Step 1: Get the ZIP code data from OpenStreetMap via Overpass API
zipcode_boundaries = get_la_zipcode_boundaries()

# Step 2: Process the data and store them in a dictionary
if zipcode_boundaries:
    zipcode_dict = process_zipcode_boundaries(zipcode_boundaries)

    # Step 3: Write the ZIP code center points to a CSV file
    write_zipcodes_to_csv(zipcode_dict)

    print(f"ZIP code data written to 'la_zipcodes.csv'. Total zipcodes: {len(zipcode_dict)}")
