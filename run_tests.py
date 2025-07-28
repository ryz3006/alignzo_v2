#!/usr/bin/env python3
"""
Simple test runner for Alignzo V2.
"""

import subprocess
import sys
import os

def run_tests():
    """Run the test suite."""
    print("🧪 Running Alignzo V2 Test Suite")
    print("=" * 40)
    
    # Install test dependencies if not already installed
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"], 
                      check=True, capture_output=True)
        print("✅ Test dependencies installed")
    except subprocess.CalledProcessError:
        print("⚠️ Could not install test dependencies, continuing...")
    
    # Run tests
    test_commands = [
        ["pytest", "tests/", "-v", "--tb=short"],
        ["pytest", "tests/test_api_gateway.py", "-v", "--tb=short"],
        ["pytest", "tests/test_integration.py", "-v", "--tb=short", "-m", "integration"]
    ]
    
    for cmd in test_commands:
        print(f"\nRunning: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, check=True)
            print("✅ Tests passed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed with exit code {e.returncode}")
            return e.returncode
    
    print("\n🎉 All tests completed!")
    return 0

if __name__ == "__main__":
    sys.exit(run_tests()) 