from crypt import methods
from flask import Flask, request, jsonify
import requests
import haversine

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "hello gobatik guys"

@app.route('/gobatik/v1/batik_store', methods=['GET'])
def batik_store():
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')

        if latitude is None or longitude is None:
            return jsonify({"error": "Latitude and longitude are required."}), 400

        url = (f"https://maps.googleapis.com/maps/api/place/textsearch/json?location={latitude}%2C{longitude}&query=batik%20store&radius=10000&key=AIzaSyD43mDPRg4B-RanFfR3pGBF9Jmj1RHqByM&rankby=prominence")

        response = requests.get(url)

        if response.status_code == 200:
            api_data = response.json()
            for store in api_data['results']:
                distance = haversine.get_distance(float(latitude), float(longitude), store['geometry']['location']['lat'], store['geometry']['location']['lng'])
                formated_distance = "{:.2f}".format(distance)
                store['distance'] = float(formated_distance)
            sorted_data = sorted(api_data['results'], key=lambda x: x['distance'])
            return jsonify(sorted_data)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
