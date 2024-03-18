import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS

#Features for price model
features1 = ["bedrooms", "bathrooms", "garages", "landArea", "floorArea", "cbdDistance", "nearestStationDistance", "postCode", "nearestSchoolDistance"]

#Features for distance models
features2 = ["bedrooms", "bathrooms", "garages", "landArea", "floorArea", "postCode"]

app = Flask(__name__)
CORS(app)

#Loading all the pickle files
scaler_price = pickle.load(open("scaler_price_model.pkl", "rb"))
scaler_others = pickle.load(open("scaler_others_model.pkl", "rb"))
price_model = pickle.load(open("price_model.pkl", "rb"))
cbd_model = pickle.load(open("cbd_model.pkl", "rb"))
station_model = pickle.load(open("station_model.pkl", "rb"))
school_model = pickle.load(open("school_model.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    
    #Getting data from the user
    user_data = request.get_json()
    
    #Processing and normalizing the features for the distance models
    float_features2 = [float(user_data[x]) for x in features2]
    normalized_features2 = scaler_others.transform([float_features2])
    cbd_dist = cbd_model.predict(normalized_features2)[0]
    station_dist = station_model.predict(normalized_features2)[0]
    school_dist = school_model.predict(normalized_features2)[0]
    
    #Updating user data with the predicted values 
    user_data_copy = user_data.copy()
    user_data_copy["cbdDistance"] = cbd_dist
    user_data_copy["nearestStationDistance"] = station_dist
    user_data_copy["nearestSchoolDistance"] = school_dist
    
    #Processing and normalizing the features for the distance models
    float_features1 = [float(user_data_copy[x]) for x in features1]
    normalized_features1 = scaler_price.transform([float_features1])
    price = price_model.predict(normalized_features1)[0]
    
    #Categorize house based on price
    if price < 415000:
        price_category = "LOW"
        
    elif price >= 415000 and price < 755000:
        price_category = "MEDIUM"
        
    elif price >= 755000:
        price_category = "HIGH"
    
    #Returning predictions results in JSON format
    return jsonify({
    "price": "{:.2f}".format(price),
    "category": price_category,
    "cbdDistance": "{:.2f}".format(cbd_dist),
    "nearestStationDistance": "{:.2f}".format(station_dist),
    "nearestSchoolDistance": "{:.2f}".format(school_dist*1000)
    }), 200

#Running the flask application
if __name__ == "__main__":
    app.run(port=8000)
    