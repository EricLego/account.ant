import pytest
from app import app
#from models.password import hash_pass

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

def test_login_success(client):
    """Test login with valid credentials."""
    # First, create a user
    client.post(
        "/user/create",
        json={
            "first_name": "Eric",
            "last_name": "Lego",
            "email": "validuser@example.com",
            "password": "securepassword",
            "role": 1
        }
    )

    # Then, try logging in
    response = client.post(
        "/auth/login",
        json={"username": "validuser@example.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json

def test_login_invalid_password(client):
    """Test login with an invalid password."""
    response = client.post(
        "/auth/login",
        json={"username": "validuser@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json["message"] == "Invalid username or password"

def test_login_nonexistent_user(client):
    """Test login with a non-existent user."""
    response = client.post(
        "/auth/login",
        json={"username": "doesnotexist@example.com", "password": "irrelevant"}
    )
    assert response.status_code == 401
    assert response.json["message"] == "Invalid username or password"

def test_token_validation(client):
    """Test that an invalid token fails authentication."""
    response = client.post(
        "/auth/validate",
        json={"token": "invalid_token"}
    )
    assert response.status_code == 401
    assert response.json["message"] == "Invalid token"
