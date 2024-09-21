import csv
import requests
import json
from collections import defaultdict

# API request
url = "https://realtor16.p.rapidapi.com/property"
querystring = {"property_id": "1497548641"}

headers = {
    "x-rapidapi-key": "07d422d02fmsh0c69f45783b8aa6p1ddfb1jsnf820f3d13262",
    "x-rapidapi-host": "realtor16.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# Flattening the JSON for relevant data
flattened_data = defaultdict(dict)

# Extract the home description details
description = data['home']['description']
flattened_data['home']['beds'] = description.get('beds', 'N/A')
flattened_data['home']['baths'] = description.get('baths', 'N/A')
flattened_data['home']['sqft'] = description.get('sqft', 'N/A')
flattened_data['home']['lot_sqft'] = description.get('lot_sqft', 'N/A')
flattened_data['home']['year_built'] = description.get('year_built', 'N/A')

# Extract the property location
location = data['home']['location']['address']
flattened_data['location']['street_address'] = location.get('line', 'N/A')
flattened_data['location']['city'] = location.get('city', 'N/A')
flattened_data['location']['state'] = location.get('state', 'N/A')
flattened_data['location']['postal_code'] = location.get('postal_code', 'N/A')

# Extract price information
flattened_data['price']['list_price'] = data['home'].get('list_price', 'N/A')
flattened_data['price']['price_per_sqft'] = data['home'].get('price_per_sqft', 'N/A')

# Extract school information
schools = data['home']['schools']['schools']
for idx, school in enumerate(schools):
    flattened_data[f'school_{idx+1}']['name'] = school.get('name', 'N/A')
    flattened_data[f'school_{idx+1}']['distance_in_miles'] = school.get('distance_in_miles', 'N/A')
    flattened_data[f'school_{idx+1}']['rating'] = school.get('rating', 'N/A')

# Write to CSV
with open('property_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write headers (fields)
    writer.writerow(["Category", "Attribute", "Value"])
    
    # Write flattened data
    for category, attributes in flattened_data.items():
        for attribute, value in attributes.items():
            writer.writerow([category, attribute, value])

print("Data successfully written to property_data.csv")
