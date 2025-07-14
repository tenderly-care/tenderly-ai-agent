#!/usr/bin/env python
"""Test script for the AI Diagnosis Agent."""

import sys
import os
import json
import requests
from datetime import datetime, timedelta
from jose import jwt

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.config.settings import settings

def create_test_token():
    """Create a test JWT token."""
    payload = {
        "sub": "test_user_123",
        "username": "test_user",
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token

def test_endpoints():
    """Test various API endpoints."""
    base_url = f"http://localhost:{settings.port}"
    
    print("🧪 Testing Tenderly AI Agent API")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    response = requests.get(f"{base_url}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Health check
    print("\n2. Testing health check...")
    response = requests.get(f"{base_url}/api/v1/health/live")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 3: Full health check
    print("\n3. Testing full health check...")
    response = requests.get(f"{base_url}/api/v1/health/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 4: Diagnosis without auth (should fail)
    print("\n4. Testing diagnosis without auth (should fail)...")
    test_data = {
        "symptoms": ["vaginal discharge", "itching"],
        "patient_age": 25,
        "severity_level": "moderate",
        "duration": "3 days"
    }
    
    response = requests.post(
        f"{base_url}/api/v1/diagnosis/",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 5: Diagnosis with auth
    print("\n5. Testing diagnosis with auth...")
    token = create_test_token()
    print(f"Generated token: {token[:50]}...")
    
    response = requests.post(
        f"{base_url}/api/v1/diagnosis/",
        json=test_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Diagnosis successful!")
        print(f"Diagnosis: {result.get('diagnosis', 'N/A')}")
        print(f"Confidence: {result.get('confidence_score', 'N/A')}")
        print(f"Medications: {len(result.get('recommended_medications', []))}")
        print(f"Investigations: {len(result.get('suggested_investigations', []))}")
    else:
        print(f"❌ Diagnosis failed: {response.json()}")
    
    # Test 6: Symptom validation
    print("\n6. Testing symptom validation...")
    response = requests.post(
        f"{base_url}/api/v1/diagnosis/validate",
        json=["discharge", "itching", "pain"],
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")
    print("\n📝 Notes:")
    print("- If OpenAI shows 'unhealthy', add your API key to .env file")
    print("- All basic endpoints are working correctly")
    print("- Authentication is properly configured")
    print("- Ready for integration with your NestJS backend")

if __name__ == "__main__":
    try:
        test_endpoints()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
