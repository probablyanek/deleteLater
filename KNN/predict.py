import joblib
import numpy as np
import pandas as pd
import requests

def email(to, body):
    url = 'https://3e0f-129-146-141-83.ngrok-free.app/send-email'

    # The data to be sent to the API
    data = {
        "body": "{}".format(body),
        "to_email": "{}".format(to)
    }

    # Sending a POST request to the API
    response = requests.post(url, json=data)

    return response.status_code

knn_loaded = joblib.load('knn_model.pkl')

def danger(nosPreg, glucose, bp, bmi, age, email):
    # Make predictions using the loaded model
    sample_data = np.array([[int(nosPreg), int(glucose), int(bp), int(bmi), int(age)]])  # Replace with actual input data
    prediction = knn_loaded.predict(sample_data)
    if prediction[0] == 1:
        email(f"{email}", f"Patient is critical. Blood glucose level: {glucose}mg/dL ")
    return prediction[0]

