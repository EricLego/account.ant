import pytest
from app import create_app

@pytest.fixture
def client():
    # Again, use the fixture from conftest.py if possible.
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
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
    json_data = response.get_json()
    assert json_data.get("message") == "User created successfully"

def test_create_user_duplicate(client):
    """Test that creating a user with an existing email fails."""
    # Create the user for the first time
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
    # Attempt to create again
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
    json_data = response.get_json()
    assert json_data.get("message") == "User already exists"

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
    json_data = response.get_json()
    assert "Missing or empty field" in json_data.get("message", "")
