from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)
CORS(app)

df = pd.read_excel('locations.xlsx')

# ensure coordinates are numeric
df['latMin'] = pd.to_numeric(df['latMin'], errors='coerce')
df['latMax'] = pd.to_numeric(df['latMax'], errors='coerce')
df['lngMin'] = pd.to_numeric(df['lngMin'], errors='coerce')
df['lngMax'] = pd.to_numeric(df['lngMax'], errors='coerce')


def find_grid_location(lat, lng):
    # Filter the DataFrame based on lat/lng bounds
    location_row = df[(df['latMin'] <= lat) & (df['latMax'] >= lat) &
                      (df['lngMin'] >= lng) & (df['lngMax'] <= lng)]
        
    if not location_row.empty:
        return location_row.index[0]  # Return the index (location ID) of the matching row
    return None

@app.route('/rank-areas', methods=['POST'])
def rank_areas():
    try:
        # Get the ZIP code from the request body
        data = request.json
        lat = data.get('lat')
        lng = data.get('lng')

        location_index = find_grid_location(lat, lng)

        if location_index is None:
            return jsonify({"status": "error", "message": "Location not found in grid"}), 404
        
        # Normalize the scores for KNN (including the median house price)
        scaler = StandardScaler()
        scores = df[['restaurants', 'bus_stops']]
        normalized_scores = scaler.fit_transform(scores)

        # Fit KNN model using all three features: restaurants, bus_stops, and median_house_price
        knn = NearestNeighbors(n_neighbors=6)  # Find 6 neighbors to include the target + 5 nearest neighbors
        knn.fit(normalized_scores)

        # Step 3: Perform KNN to find the 5 nearest neighbors
        distances, indices = knn.kneighbors(normalized_scores[location_index].reshape(1,-1))

        # Get the lat/lng bounds of the 5 nearest neighbors
        nearest_locations = df.iloc[indices[0]]

        # Step 5: Calculate the central point for each location
        central_points = []
        for _, row in nearest_locations.iterrows():
            lat_center = (row['latMin'] + row['latMax']) / 2
            lng_center = (row['lngMin'] + row['lngMax']) / 2
            central_points.append({
                "lat": lat_center,
                "lng": lng_center,
                "price": row['median_house_price']
            })

        # Return the list of central points to the front end
        return jsonify({
            "status": "success",
            "data": central_points
        }), 200


    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
