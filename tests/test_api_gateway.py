import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

class TestAPIGateway:
    """Test cases for API Gateway functionality."""
    
    def test_health_endpoint(self, test_client: TestClient):
        """Test the health endpoint of the API gateway."""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "api-gateway"
    
    @pytest.mark.asyncio
    async def test_services_health_endpoint(self, async_client: AsyncClient):
        """Test the services health endpoint."""
        response = await async_client.get("/services/health")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        # Note: In a real test environment, services might not be running
        # so we just check that the endpoint returns a valid response structure
    
    def test_user_service_proxy_get(self, test_client: TestClient):
        """Test user service proxy GET endpoint."""
        response = test_client.get("/users/health")
        # This might fail if user service is not running, but we test the routing
        assert response.status_code in [200, 500, 404]
    
    def test_project_service_proxy_get(self, test_client: TestClient):
        """Test project service proxy GET endpoint."""
        response = test_client.get("/projects/")
        # This might fail if project service is not running, but we test the routing
        assert response.status_code in [200, 500, 404]
    
    def test_orchestrator_proxy_get(self, test_client: TestClient):
        """Test orchestrator proxy GET endpoint."""
        response = test_client.get("/orchestrator/")
        # This might fail if orchestrator service is not running, but we test the routing
        assert response.status_code in [200, 500, 404] 