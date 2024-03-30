"""
API server module test
"""
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """
    Fixture to get API client
    """
    api_client = TestClient(app)
    return api_client

def test_get(client):
    """
    Test GET endpoint "/"
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, welcome to our app!"}

def test_get_malformed(client):
    """
    Test GET endpoint with wrong URL
    """
    response = client.get("/wrong_url")
    assert response.status_code != 200

def test_post_above(client):
    """
    Test POST endpoint with input values indicating income >50K
    """
    response = client.post("/", json={
        "age": 60,
        "workclass": "Private",
        "education": "Doctorate",
        "maritalStatus": "Divorced",
        "occupation": "Transport-moving",
        "relationship": "Not-in-family",
        "race": "White",
        "sex": "Male",
        "hoursPerWeek": 76,
        "nativeCountry": "United-States"
    })
    assert response.status_code == 200
    assert response.json() == {"prediction": "<=50K"}

def test_post_below(client):
    """
    Test POST endpoint with input values indicating income <=50K
    """
    response = client.post("/", json={
        "age": 16,
        "workclass": "Private",
        "education": "HS-grad",
        "maritalStatus": "Never-married",
        "occupation": "Other-service",
        "relationship": "Own-child",
        "race": "Black",
        "sex": "Male",
        "hoursPerWeek": 40,
        "nativeCountry": "United-States"
    })
    assert response.status_code == 200
    assert response.json() == {"prediction": "<=50K"}

def test_post_malformed(client):
    """
    Test POST endpoint with input values containing errors
    """
    response = client.post("/", json={
        "age": 32,
        "workclass": "Private",
        "education": "Some-college",
        "maritalStatus": "ERROR",
        "occupation": "Exec-managerial",
        "relationship": "Husband",
        "race": "Black",
        "sex": "Male",
        "hoursPerWeek": 60,
        "nativeCountry": "United-States"
    })
    assert response.status_code != 200
