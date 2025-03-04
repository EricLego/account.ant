import pytest
from app import create_app
import os

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    # You may also configure a test database here if needed.
    with app.test_client() as client:
        yield client
