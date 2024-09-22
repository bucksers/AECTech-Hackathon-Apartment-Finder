from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Your API route
@app.route('/rank-areas', methods=['POST'])
def rank_areas():
    try:
        data = request.json
        zip_code = data.get('zip')
        price = data.get('price')
        property_type = data.get('propertyType')

        # Mock data (replace with your real ranking logic)
        results = [
            {"area": "Area 1", "similarity_score": 90},
            {"area": "Area 2", "similarity_score": 85},
            {"area": "Area 3", "similarity_score": 80},
        ]
        return jsonify({"status": "success", "data": results}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
