"""
Test module for the user service endpoints.
This module contains tests for the FastAPI user service, 
including testing the main endpoint, creating a user, and reading user details.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_index():
    """
    Test the root endpoint ("/").
    Ensures the endpoint returns a 200 status code and the expected JSON response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Order service"}
