"""
Test module for the user service endpoints.
This module contains tests for the FastAPI user service, 
including testing the main endpoint, creating a user, and reading user details.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    """
    Test the root endpoint ("/").
    Ensures the main endpoint returns a 200 status code
    and the expected JSON response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "User service"}


def test_create_user():
    """
    Test the user creation endpoint ("/user").
    Ensures that a user can be created with valid data
    and the correct status code and response are returned.
    """
    response = client.post(
        "/user",
        json={"name": "Test User"},
    )
    assert response.status_code == 200


def test_read_user():
    """
    Test the read user endpoint ("/user/{id}").
    Ensures that user details can be retrieved using a valid user ID.
    """
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test User", "orders": []}
