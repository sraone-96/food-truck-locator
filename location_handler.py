from math import radians
import numpy as np
from sklearn.metrics.pairwise import haversine_distances
req_parameters = ["locationid", "FacilityType", "Address", "FoodItems", "Latitude", "Longitude","Applicant", "Status"]

def get_nearest_data(data, loc_id_list, lat_query, lon_query, radius):
    nearest_ids = find_nearest_coordinates(loc_id_list, lat_query,lon_query,radius)
    extracted_data = [extract_req_data(data,x) for x in nearest_ids]
    return extracted_data

def extract_req_data(data, x):
    req_data = {k:v for k,v in data[x].items() if k in req_parameters}
    if(req_data["Status"]=="APPROVED"):
        req_data["Status"] = "Open"
    elif( req_data["Status"]=="ISSUED"):
        req_data["Status"] = "Opening Soon"
    elif (req_data["Status"] == "EXPIRED" or req_data["Status"] == "SUSPEND" ):
        req_data["Status"] = "permanently closed"
    else:
        req_data["Status"] = "Might open in few months"

    req_data["Name"] = req_data["Applicant"]
    req_data.pop('Applicant')
    return req_data


def find_nearest_coordinates(lat_lon_id_list, lat_query, lon_query, radius):
    lat_list = [radians(lat_lon_id[0]) for lat_lon_id in lat_lon_id_list]
    lon_list = [radians(lat_lon_id[1]) for lat_lon_id in lat_lon_id_list]
    ids = [lat_lon_id[2] for lat_lon_id in lat_lon_id_list]

    # Convert the query latitude and longitude to radians
    lat_query, lon_query = radians(lat_query), radians(lon_query)

    # Compute distances using the Haversine formula
    distances = haversine_distances(np.array([lat_query, lon_query]).reshape(1, -1),
                                    np.vstack([lat_list, lon_list]).T)

    distances_in_miles = (distances.flatten()) * 3958.756 
    # print(distances_in_miles.shape)
    # Filter coordinates within the specified radius
    indices = np.where(distances_in_miles <= radius)[0]

    # Return the ids of the nearest coordinates within the radius
    nearest_ids = [ids[i] for i in indices]
    return nearest_ids