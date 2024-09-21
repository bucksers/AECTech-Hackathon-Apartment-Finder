import requests
import csv

# API request setup
url = "https://realtor16.p.rapidapi.com/forrent"
querystring = {"location": "los angeles"}
headers = {
    "x-rapidapi-key": "07d422d02fmsh0c69f45783b8aa6p1ddfb1jsnf820f3d13262",
    "x-rapidapi-host": "realtor16.p.rapidapi.com"
}

# Send the request
response = requests.get(url, headers=headers, params=querystring)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Open a CSV file to write to
    with open('rental_properties.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow([
            "Name", "Min Price", "Max Price", "Address", "City", "State", "Postal Code", "Beds", "Baths", "URL"
        ])

        # Iterate over the listings and extract relevant information
        for listing in data.get('results', []):
            # Extract relevant fields
            name = listing.get('description', {}).get('name', 'N/A')
            price_min = listing.get('list_price_min', 'N/A')
            price_max = listing.get('list_price_max', 'N/A')
            address = listing.get('location', {}).get('address', {}).get('line', 'N/A')
            city = listing.get('location', {}).get('address', {}).get('city', 'N/A')
            state = listing.get('location', {}).get('address', {}).get('state', 'N/A')
            postal_code = listing.get('location', {}).get('address', {}).get('postal_code', 'N/A')
            beds = listing.get('description', {}).get('beds_min', 'N/A')
            baths = listing.get('description', {}).get('baths_min', 'N/A')
            url = listing.get('href', 'N/A')

            # Write the data for each property
            writer.writerow([name, price_min, price_max, address, city, state, postal_code, beds, baths, url])

    print("Data written to rental_properties.csv")
else:
    print("Failed to retrieve data:", response.status_code)
