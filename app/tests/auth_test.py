import pytest
from app import create_app

@pytest.fixture
def client():
    # Although we have a global fixture, this redefinition is optional.
    # Prefer using the conftest.py fixture to avoid duplication.
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_login_success(client):
    """Test login with valid credentials."""
    # First, create a user via the production endpoint
    create_response = client.post(
        "/user/create",
        json={
            "first_name": "Eric",
            "last_name": "Lego",
            "email": "validuser@example.com",
            "password": "securepassword",
            "role": 1
        }
    )
    assert create_response.status_code == 201

    # Then, try logging in using 'email' as the key
    response = client.post(
        "/auth/login",
        json={"email": "validuser@example.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    # Expect keys based on your auth route implementation.
    # For example, your route returns "token", "role", and "name".
    json_data = response.get_json()
    assert "token" in json_data
    assert "role" in json_data
    assert "name" in json_data

def test_login_invalid_password(client):
    """Test login with an invalid password."""
    response = client.post(
        "/auth/login",
        json={"email": "validuser@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    # Adjust the assertion to check the error key.
    json_data = response.get_json()
    assert json_data.get("error") == "Invalid email or password"

def test_login_nonexistent_user(client):
    """Test login with a non-existent user."""
    response = client.post(
        "/auth/login",
        json={"email": "doesnotexist@example.com", "password": "irrelevant"}
    )
    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data.get("error") == "Invalid email or password"

def test_token_validation(client):
    """Test that an invalid token fails authentication."""
    response = client.post(
        "/auth/validate",
        json={"token": "invalid_token"}
    )
    # According to your auth route, an invalid token should return a 401
    assert response.status_code == 401
    json_data = response.get_json()
    # The error key should contain "Invalid token" (or similar)
    assert json_data.get("error") == "Invalid token"
