# Soil Health & Fertilizer Recommendation
# Flask Web Application with Weather API

# Import Libraries

from flask import Flask, render_template, request
import pickle
import numpy as np
import requests
from core_logic import climate_advisor, generate_soil_health, generate_reason, get_cost

# City List

cities = [
    "Raipur",
    "Bilaspur",
    "Durg",
    "Bhilai",
    "Rajnandgaon",
    "Jagdalpur",
    "Korba",
    "Ambikapur",
    "Raigarh",
    "Delhi",
    "Mumbai",
    "Kolkata",
    "Chennai",
    "Bangalore",
    "Hyderabad",
    "Pune"
]

# Create Flask App

app = Flask(__name__)

# Load Trained Model
model = pickle.load(open("models/fertilizer_model.pkl", "rb"))

# Load Scaler
scaler = pickle.load(open("models/scaler.pkl", "rb"))

# Load Encoders
crop_encoder = pickle.load(open("models/crop_encoder.pkl", "rb"))
    
stage_encoder = pickle.load(open("models/stage_encoder.pkl", "rb"))

fertilizer_encoder = pickle.load(open("models/fertilizer_encoder.pkl", "rb"))

soil_encoder = pickle.load(open("models/soil_encoder.pkl", "rb"))

# Weather API Function
def get_weather(city):

    api_key = "72848d8a0185e43f7e8ab23fbb45330d"

    # API URL
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={api_key}"
        f"&units=metric"
    )

    # API Request
    response = requests.get(url)
    data = response.json()

    # Temperature
    temperature = data["main"]["temp"]

    # Humidity
    humidity = data["main"]["humidity"]

    # Rainfall
    rainfall = 0

    if "rain" in data:
        rainfall = data["rain"].get("1h", 0)

    climate_message = climate_advisor(temperature, rainfall)    

    return (
        temperature,
        humidity,
        rainfall,
        climate_message
    )


# Home Page
@app.route("/")
def home():
    return render_template("index.html", cities=cities)

# Prediction Route
@app.route("/predict", methods=["POST"])
def predict():

    # USER INPUTS
   
    city = request.form["City"]
    soil_ph = float(request.form["Soil_pH"])
    nitrogen = float(request.form["Nitrogen_Level"])
    phosphorus = float(request.form["Phosphorus_Level"])
    potassium = float(request.form["Potassium_Level"])
    crop_type = request.form["Crop_Type"]
    growth_stage = request.form["Crop_Growth_Stage"]

    # WEATHER DATA
    temperature, humidity, rainfall, climate_message = get_weather(city)

    # ENCODING
    crop_encoded = crop_encoder.transform([crop_type])[0]
    stage_encoded = stage_encoder.transform([growth_stage])[0]

    # INPUT ARRAY
    input_data = np.array([[
        soil_ph,
        nitrogen,
        phosphorus,
        potassium,
        temperature,
        humidity,
        rainfall,
        crop_encoded,
        stage_encoded
    ]])

    input_scaled = scaler.transform(input_data)

    # PREDICTION
    prediction = model.predict(input_scaled)

    fertilizer = fertilizer_encoder.inverse_transform(prediction)[0]

    # CORE LOGIC CALLS (FIXED LOCATION)
    soil_health_result = generate_soil_health(
        nitrogen,
        phosphorus,
        potassium,
        soil_ph
    )

    estimated_cost = get_cost(fertilizer)

    reason = generate_reason(
        nitrogen,
        phosphorus,
        potassium,
        growth_stage,
        fertilizer,
    )

    # CLIMATE LOGIC
    climate_message = climate_advisor(temperature, rainfall)

    # OUTPUT
    return render_template(
        "result.html",
        fertilizer=fertilizer,
        soil_health=soil_health_result,
        estimated_cost=estimated_cost,
        reason=reason,
        climate_message=climate_message,
        temperature=temperature,
        humidity=humidity,
        rainfall=rainfall,
        city=city
    )

@app.route("/weather")
def weather():

    city = request.args.get("city")

    temperature, humidity, rainfall, climate_message = get_weather(city)

    return render_template(
        "weather.html",
        city=city,
        temperature=temperature,
        humidity=humidity,
        rainfall=rainfall,
        climate_message=climate_message
    )

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True )