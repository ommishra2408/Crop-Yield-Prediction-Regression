from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import os

app = Flask(__name__)


# Load trained model
model_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "model.pkl"
)

with open(model_path, "rb") as file:
    model = pickle.load(file)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Prediction API
@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        crop = data["crop"]
        area = float(data["area"])
        rainfall = float(data["rainfall"])
        temperature = float(data["temperature"])
        fertilizer = float(data["fertilizer"])
        irrigation = float(data["irrigation"])
        soil_ph = float(data["soil_ph"])

        # Create input DataFrame
        input_data = pd.DataFrame({
            "Crop": [crop],
            "Area": [area],
            "Rainfall": [rainfall],
            "Temperature": [temperature],
            "Fertilizer": [fertilizer],
            "Irrigation": [irrigation],
            "Soil_pH": [soil_ph]
        })

        # Make prediction
        prediction = model.predict(input_data)[0]

        return jsonify({
            "success": True,
            "prediction": round(prediction, 2)
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


# Run Flask application
if __name__ == "__main__":
    app.run(debug=True)