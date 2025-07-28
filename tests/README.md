# Alignzo V2 Test Suite

This directory contains the comprehensive test suite for the Alignzo V2 microservices platform.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Pytest configuration and fixtures
├── test_api_gateway.py      # API Gateway tests
├── test_integration.py      # Integration tests
└── README.md               # This file
```

## Test Categories

### 1. Unit Tests
- **API Gateway Tests** (`test_api_gateway.py`): Test the API gateway functionality, routing, and health endpoints.

### 2. Integration Tests
- **Service Integration** (`test_integration.py`): Test communication between microservices, database connectivity, and end-to-end workflows.

## Running Tests

### Prerequisites
1. Install test dependencies:
   ```bash
   pip install -r requirements-test.txt
   ```

2. Ensure services are running:
   ```bash
   docker-compose up -d
   ```

### Running All Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=.

# Run specific test file
pytest tests/test_api_gateway.py -v

# Run integration tests only
pytest tests/test_integration.py -v -m integration
```

### Using the Test Runner Scripts

#### Quick Test Run
```bash
python run_tests.py
```

#### Full Service Setup and Test
```bash
python scripts/start_services.py
```

## Test Configuration

The test configuration is defined in:
- `pytest.ini`: Pytest configuration
- `conftest.py`: Test fixtures and setup
- `requirements-test.txt`: Test dependencies

## Test Fixtures

Available fixtures in `conftest.py`:
- `test_client`: FastAPI test client
- `async_client`: Async HTTP client
- `sample_user_data`: Sample user data for testing
- `sample_project_data`: Sample project data for testing
- `sample_test_data`: Sample test data for testing

## Service Health Checks

The integration tests include health checks for all services:
- API Gateway: http://localhost:8004
- User Service: http://localhost:8000
- Orchestrator: http://localhost:8002
- Project Service: http://localhost:8003
- Logging Service: http://localhost:8001

## Adding New Tests

1. Create a new test file following the naming convention: `test_*.py`
2. Use the existing fixtures from `conftest.py`
3. Add appropriate markers for test categorization
4. Include both positive and negative test cases
5. Add proper error handling and assertions

## Test Best Practices

1. **Isolation**: Each test should be independent and not rely on other tests
2. **Cleanup**: Clean up any test data after tests complete
3. **Descriptive Names**: Use clear, descriptive test function names
4. **Error Messages**: Provide meaningful error messages in assertions
5. **Async Support**: Use `pytest.mark.asyncio` for async tests
6. **Service Dependencies**: Handle cases where services might not be running

## Troubleshooting

### Common Issues

1. **Services not running**: Ensure all services are started with `docker-compose up -d`
2. **Database connection issues**: Check if PostgreSQL is running and accessible
3. **Port conflicts**: Ensure no other services are using the required ports (8000-8004)
4. **Dependencies missing**: Install test dependencies with `pip install -r requirements-test.txt`

### Debug Mode

Run tests with verbose output for debugging:
```bash
pytest tests/ -v -s --tb=long
```

## Continuous Integration

The test suite is designed to work with CI/CD pipelines. The `scripts/start_services.py` script can be used in CI environments to:
1. Start all services
2. Wait for services to be healthy
3. Run the test suite
4. Report results 