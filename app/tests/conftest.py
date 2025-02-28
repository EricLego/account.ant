import pytest
from app import create_app
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()
