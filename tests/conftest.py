import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test configuration
TEST_DATABASE_URL = "postgresql://alignzo:alignzo@localhost:5432/alignzo_v2_test"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def test_client():
    """Create a test client for FastAPI applications."""
    from api_gateway.app.main import app
    return TestClient(app)

@pytest.fixture
async def async_client():
    """Create an async test client."""
    from api_gateway.app.main import app
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpassword123"
    }

@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        "name": "Test Project",
        "description": "A test project for testing purposes"
    }

@pytest.fixture
def sample_test_data():
    """Sample test data for testing."""
    return {
        "name": "Sample Test",
        "type": "functional",
        "description": "A sample test for testing purposes"
    } 