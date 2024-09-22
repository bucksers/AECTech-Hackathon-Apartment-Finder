import csv

# Constants
MILES_PER_LAT_DEGREE = 69.0  # Approximately 69 miles per degree of latitude
LAT_STEP = 1 / MILES_PER_LAT_DEGREE  # Latitude step for 1 mile
LONGITUDE_STEP_AT_34N = 1 / 57.3  # Approximate miles per degree of longitude at 34° N latitude

# Los Angeles County Boundaries (approximate)
START_LAT = 33.7037  # Southern latitude of LA County
END_LAT = 34.8233  # Northern latitude of LA County
START_LON = -119.9423  # Western longitude of LA County
END_LON = -117.6460  # Eastern longitude of LA County

def generate_lat_lon_squares_fixed(start_lat, end_lat, start_lon, end_lon, lat_step, lon_step):
    """
    Generate lat/lon boundaries for 1-mile by 1-mile squares within Los Angeles County.
    Use fixed longitude and latitude steps.
    """
    squares = []
    
    lat = start_lat
    while lat < end_lat:
        lon = start_lon
        while lon < end_lon:
            # Define the square boundary
            square = {
                'min_lat': lat,
                'min_lon': lon,
                'max_lat': lat + lat_step,
                'max_lon': lon + lon_step
            }
            
            squares.append(square)
            
            # Move to the next square in longitude
            lon += lon_step
        
        # Move to the next square in latitude
        lat += lat_step
    
    return squares

def write_squares_to_csv(squares, filename='la_county_squares_fixed.csv'):
    """
    Write the latitude/longitude boundaries of the grid squares to a CSV file,
    adding an index column.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header with an index column
        writer.writerow(["Index", "Min Latitude", "Min Longitude", "Max Latitude", "Max Longitude"])
        
        # Write the square data with an index
        for index, square in enumerate(squares, start=1):
            writer.writerow([index, square['min_lat'], square['min_lon'], square['max_lat'], square['max_lon']])

# Step 1: Generate the grid of 1-mile by 1-mile squares within Los Angeles County
squares = generate_lat_lon_squares_fixed(START_LAT, END_LAT, START_LON, END_LON, LAT_STEP, LONGITUDE_STEP_AT_34N)

# Step 2: Write the square boundaries to a CSV file with an index
write_squares_to_csv(squares)

print(f"Grid of squares written to 'la_county_squares_fixed.csv'. Total squares: {len(squares)}")
