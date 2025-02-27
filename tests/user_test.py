import pytest
from app import app
from config.db_config import get_db_connection

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

def test_create_user_success(client):
    """Test creating a user successfully."""
    response = client.post(
        "/user/create",
        json={
            "first_name": "Eric",
            "last_name": "Lego",
            "email": "testuser@example.com",
            "password": "securepassword",
            "role": 1
        }
    )
    assert response.status_code == 201
    assert response.json["message"] == "User created successfully"

def test_create_user_duplicate(client):
    """Test that creating a user with an existing email fails."""
    client.post(
        "/user/create",
        json={
            "first_name": "Eric",
            "last_name": "Lego",
            "email": "duplicate@example.com",
            "password": "securepassword",
            "role": 1
        }
    )
    response = client.post(
        "/user/create",
        json={
            "first_name": "Eric",
            "last_name": "Lego",
            "email": "duplicate@example.com",
            "password": "securepassword",
            "role": 1
        }
    )
    assert response.status_code == 400
    assert response.json["message"] == "User already exists"

def test_create_user_missing_field(client):
    """Test that missing a required field results in a 400 error."""
    response = client.post(
        "/user/create",
        json={
            "first_name": "Eric",
            "email": "missing@example.com",
            "password": "securepassword",
            "role": 1
        }
    )
    assert response.status_code == 400
    assert "Missing or empty field" in response.json["message"]
