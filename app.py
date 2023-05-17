from flask import Flask, request
from location_handler import get_nearest_data
import csv

data_file = '../data.csv'
app = Flask(__name__)

# Global variable to store the data
data = {}
loc_id_list = []

def load_data():
    global data
    with open(data_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row['locationid']  # Replace 'KeyColumn' with the actual column name you want to use as the key
            data[key] = row
            loc_id_list.append([float(row['Latitude']),float(row['Longitude']),key])

load_data()

@app.route('/', methods=['GET'])
def hello_world():
    print('Request received')
    # ... your code ...
    return 'Hello, world!'

@app.route('/nearest', methods=['POST'])
def post_data():
    if request.method == 'POST':
        try:
            req_data = request.get_json()
            lat_query = (req_data['lat'])
            lon_query = (req_data['lon'])
            global data
            return get_nearest_data(data, loc_id_list, lat_query ,lon_query), 200
        except Exception as e:
            return str(e), 400  # Return an error response
    else:
        return 'Method not allowed', 405  # Return a method not allowed response


# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run()



