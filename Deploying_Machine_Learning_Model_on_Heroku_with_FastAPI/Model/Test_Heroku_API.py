"""
Test Heroku Api
Author: Rajesh Daravath
"""
import requests

# Define the input data
input_data = {
    "age": 32,
    "workclass": "State-gov",
    "education": "Some-college",
    "maritalStatus": "Married-civ-spouse",
    "occupation": "Exec-managerial",
    "relationship": "Husband",
    "race": "White",
    "sex": "Male",  # Ensure the gender value matches the Pydantic model
    "hoursPerWeek": 40,
    "nativeCountry": "United-States"
}

# Send POST request to the API
response = requests.post('https://mlops-salaries.herokuapp.com', json=input_data)

# Check if the response status code is 200
assert response.status_code == 200

# Print response status code and body
print("Response code: %s" % response.status_code)
print("Response body: %s" % response.json())
