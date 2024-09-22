import requests
import csv

def get_similar_homes(zip_code):
    url = "https://zillow-com4.p.rapidapi.com/properties/similar-homes"

    querystring = {"zpid": zip_code}

    headers = {
        "x-rapidapi-key": "07d422d02fmsh0c69f45783b8aa6p1ddfb1jsnf820f3d13262",
        "x-rapidapi-host": "zillow-com4.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def write_to_csv(data):
    # Open a CSV file to write to
    with open('similar_homes_output.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(["Price", "Bedrooms", "Bathrooms", "Living Area (sqft)", "Street Address", "City", "State", "ZIP Code", "Home Type", "URL"])
        
        # Loop through each property in the 'data' field
        for home in data['data']:
            price = home.get('price', 'N/A')
            bedrooms = home.get('bedrooms', 'N/A')
            bathrooms = home.get('bathrooms', 'N/A')
            living_area = home.get('livingArea', 'N/A')
            address = home.get('address', {})
            street_address = address.get('streetAddress', 'N/A')
            city = address.get('city', 'N/A')
            state = address.get('state', 'N/A')
            zipcode = address.get('zipcode', 'N/A')
            home_type = home.get('homeType', 'N/A')
            url = home.get('hdpUrl', 'N/A')
            
            # Write the row for each property
            writer.writerow([price, bedrooms, bathrooms, living_area, street_address, city, state, zipcode, home_type, f"https://www.zillow.com{url}"])

# Example usage of the function
zip_code = "90034"  # Example 5-digit ZIP code
response_data = get_similar_homes(zip_code)

# Write the response data to a CSV file
write_to_csv(response_data)

print("Data has been written to similar_homes_output.csv")
