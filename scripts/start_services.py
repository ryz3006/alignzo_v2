#!/usr/bin/env python3
"""
Script to start Alignzo V2 services and run tests.
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_service_health(service_name, port):
    """Check if a service is healthy."""
    import requests
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main function to start services and run tests."""
    print("🚀 Starting Alignzo V2 Services and Test Suite")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Step 1: Start the services using docker-compose
    print("\n📦 Starting services with Docker Compose...")
    success, stdout, stderr = run_command("docker-compose up -d --build")
    
    if not success:
        print(f"❌ Failed to start services: {stderr}")
        return 1
    
    print("✅ Services started successfully")
    
    # Step 2: Wait for services to be ready
    print("\n⏳ Waiting for services to be ready...")
    services = [
        ("logging-service", 8001),
        ("user-service", 8000),
        ("orchestrator", 8002),
        ("project-service", 8003),
        ("api-gateway", 8004)
    ]
    
    max_wait = 60  # Maximum wait time in seconds
    wait_time = 0
    
    while wait_time < max_wait:
        all_ready = True
        for service_name, port in services:
            if not check_service_health(service_name, port):
                all_ready = False
                print(f"⏳ Waiting for {service_name} on port {port}...")
                break
        
        if all_ready:
            print("✅ All services are ready!")
            break
        
        time.sleep(5)
        wait_time += 5
    
    if wait_time >= max_wait:
        print("⚠️ Some services may not be fully ready, but continuing with tests...")
    
    # Step 3: Install test dependencies
    print("\n📚 Installing test dependencies...")
    success, stdout, stderr = run_command("pip install -r requirements-test.txt")
    
    if not success:
        print(f"❌ Failed to install test dependencies: {stderr}")
        return 1
    
    print("✅ Test dependencies installed")
    
    # Step 4: Run the test suite
    print("\n🧪 Running test suite...")
    test_commands = [
        "pytest tests/ -v --tb=short",
        "pytest tests/test_api_gateway.py -v --tb=short",
        "pytest tests/test_integration.py -v --tb=short -m integration"
    ]
    
    for cmd in test_commands:
        print(f"\nRunning: {cmd}")
        success, stdout, stderr = run_command(cmd)
        
        if success:
            print("✅ Tests passed")
            print(stdout)
        else:
            print("❌ Tests failed")
            print(stderr)
    
    # Step 5: Show service status
    print("\n📊 Service Status:")
    print("-" * 30)
    for service_name, port in services:
        status = "✅ Healthy" if check_service_health(service_name, port) else "❌ Unhealthy"
        print(f"{service_name}: {status} (http://localhost:{port})")
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Access API Gateway: http://localhost:8004")
    print("2. Access User Service: http://localhost:8000")
    print("3. Access Orchestrator: http://localhost:8002")
    print("4. Access Project Service: http://localhost:8003")
    print("5. Access Logging Service: http://localhost:8001")
    print("\nTo stop services: docker-compose down")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 