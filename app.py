from flask import Flask, render_template, request
import joblib

app = Flask(__name__)
model = joblib.load("random_forest_regressor.joblib")

# Load the saved LabelEncoders
sex_encoder = joblib.load("sex_encoder.joblib")
smoker_encoder = joblib.load("smoker_encoder.joblib")
region_encoder = joblib.load("region_encoder.joblib")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Extract data from form
    age = request.form.get('age', type=int)
    sex = sex_encoder.transform([request.form['sex']])[0]
    bmi = request.form.get('bmi', type=float)
    children = request.form.get('children', type=int)
    smoker = smoker_encoder.transform([request.form['smoker']])[0]
    region = region_encoder.transform([request.form['region']])[0]

    # Prepare the data for prediction
    features = [[age, sex, bmi, children, smoker, region]]

    # Make prediction
    prediction = model.predict(features)[0]

    formatted_prediction = "${:.2f}".format(prediction)
    # Return result
    return render_template('index.html', prediction=formatted_prediction)

if __name__ == "__main__":
    app.run(debug=True)

