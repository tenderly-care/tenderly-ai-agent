#!/usr/bin/env python3
"""
Test Authentication Keys
Verifies that generated keys work properly for authentication
"""

import json
import requests
import sys
from datetime import datetime
from jose import jwt

def load_keys(filename="tenderly-keys.json"):
    """Load generated keys from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Keys file '{filename}' not found. Run generate-tenderly-keys.py first.")
        sys.exit(1)

def create_test_jwt_token(jwt_secret):
    """Create a test JWT token for verification"""
    now = int(datetime.now().timestamp())
    payload = {
        "sub": "test-service",
        "username": "test-user",
        "exp": now + 3600,  # 1 hour
        "iat": now,
        "aud": "ai-diagnosis-service",
        "iss": "tenderly-backend",
        "service": True
    }
    
    return jwt.encode(payload, jwt_secret, algorithm="HS256")

def test_api_key_auth(api_key):
    """Test API key authentication"""
    print("🔑 Testing API Key Authentication...")
    
    url = "http://localhost:8000/api/v1/diagnosis/structure"
    headers = {
        "X-API-Key": api_key,
        "X-Service-Name": "tenderly-backend",
        "Content-Type": "application/json"
    }
    
    payload = {
        "structured_request": {
            "patient_profile": {
                "age": 28,
                "request_id": "test-api-key-auth",
                "timestamp": datetime.now().isoformat() + "Z"
            },
            "primary_complaint": {
                "main_symptom": "test_symptom",
                "duration": "1 day",
                "severity": "mild"
            },
            "symptom_specific_details": {
                "symptom_characteristics": {
                    "test": "value"
                }
            },
            "reproductive_history": {
                "pregnancy_status": {"could_be_pregnant": False},
                "sexual_activity": {"sexually_active": True},
                "menstrual_history": {"cycle_frequency": 28}
            },
            "associated_symptoms": {
                "pain": {"pelvic_pain": "none"},
                "systemic": {"fatigue": "mild"}
            },
            "medical_context": {
                "current_medications": [],
                "recent_medications": [],
                "medical_conditions": [],
                "allergies": [],
                "family_history": []
            },
            "healthcare_interaction": {
                "previous_consultation": False,
                "investigations_done": False
            },
            "patient_concerns": {
                "main_worry": "Test concern",
                "impact_on_life": "mild"
            }
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ API Key authentication successful!")
            return True
        elif response.status_code == 401:
            print(f"   ❌ API Key authentication failed: {response.json()}")
            return False
        elif response.status_code == 422:
            print("   ⚠️  API Key authenticated but request validation failed (this is expected for test data)")
            return True
        else:
            print(f"   ⚠️  Unexpected response: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed - is the AI Agent server running on localhost:8000?")
        return False
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
        return False

def test_jwt_auth(jwt_secret):
    """Test JWT token authentication"""
    print("🔐 Testing JWT Authentication...")
    
    # Create test JWT token
    token = create_test_jwt_token(jwt_secret)
    print(f"   Generated test JWT: {token[:50]}...")
    
    url = "http://localhost:8000/api/v1/diagnosis/structure"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "structured_request": {
            "patient_profile": {
                "age": 28,
                "request_id": "test-jwt-auth", 
                "timestamp": datetime.now().isoformat() + "Z"
            },
            "primary_complaint": {
                "main_symptom": "test_symptom",
                "duration": "1 day",
                "severity": "mild"
            },
            "symptom_specific_details": {
                "symptom_characteristics": {
                    "test": "value"
                }
            },
            "reproductive_history": {
                "pregnancy_status": {"could_be_pregnant": False},
                "sexual_activity": {"sexually_active": True},
                "menstrual_history": {"cycle_frequency": 28}
            },
            "associated_symptoms": {
                "pain": {"pelvic_pain": "none"},
                "systemic": {"fatigue": "mild"}
            },
            "medical_context": {
                "current_medications": [],
                "recent_medications": [],
                "medical_conditions": [],
                "allergies": [],
                "family_history": []
            },
            "healthcare_interaction": {
                "previous_consultation": False,
                "investigations_done": False
            },
            "patient_concerns": {
                "main_worry": "Test concern",
                "impact_on_life": "mild"
            }
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ JWT authentication successful!")
            return True
        elif response.status_code == 401:
            print(f"   ❌ JWT authentication failed: {response.json()}")
            return False
        elif response.status_code == 422:
            print("   ⚠️  JWT authenticated but request validation failed (this is expected for test data)")
            return True
        else:
            print(f"   ⚠️  Unexpected response: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed - is the AI Agent server running on localhost:8000?")
        return False
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
        return False

def test_service_health():
    """Test service health endpoints"""
    print("🏥 Testing Service Health...")
    
    # Test backend health
    try:
        response = requests.get("http://localhost:3000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend service is healthy")
        else:
            print("   ⚠️  Backend service health check returned non-200")
    except:
        print("   ❌ Backend service is not accessible (expected if not running)")
    
    # Test AI agent health
    try:
        response = requests.get("http://localhost:8000/api/v1/health/live", timeout=5)
        if response.status_code == 200:
            print("   ✅ AI Agent service is healthy")
            return True
        else:
            print("   ⚠️  AI Agent service health check returned non-200")
            return False
    except:
        print("   ❌ AI Agent service is not accessible - start it first")
        return False

def main():
    """Main test function"""
    print("🧪 Tenderly Authentication Key Tester")
    print("=" * 50)
    
    # Load generated keys
    keys = load_keys()
    print(f"📄 Loaded keys from tenderly-keys.json")
    print(f"🕐 Generated at: {keys.get('GENERATED_AT')}")
    
    # Test service health first
    if not test_service_health():
        print("\n❌ Cannot run authentication tests - AI Agent service is not running")
        print("   Start it with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        sys.exit(1)
    
    print()
    
    # Test API key authentication
    api_key_success = test_api_key_auth(keys['AI_DIAGNOSIS_API_KEY'])
    
    print()
    
    # Test JWT authentication  
    jwt_success = test_jwt_auth(keys['JWT_SECRET_KEY'])
    
    print()
    print("=" * 50)
    print("🏁 Test Results Summary")
    print("=" * 50)
    
    if api_key_success and jwt_success:
        print("✅ All authentication tests PASSED!")
        print("🎉 Your new keys are working correctly!")
        print("\n📋 Next Steps:")
        print("   1. Update both service .env files with new keys")
        print("   2. Restart both services")
        print("   3. Run integration tests")
        print("   4. Monitor logs for any issues")
        print("   5. Delete tenderly-keys.json file")
    elif api_key_success or jwt_success:
        print("⚠️  Partial success - some authentication methods working")
        if not api_key_success:
            print("   ❌ API Key authentication needs attention")
        if not jwt_success:
            print("   ❌ JWT authentication needs attention")
        print("\n🔧 Check service configuration and restart services")
    else:
        print("❌ All authentication tests FAILED!")
        print("🔧 Check service configuration, keys, and ensure services are running")
    
    print(f"\n🔐 Security Reminder:")
    print(f"   • Delete test files after successful deployment")
    print(f"   • Monitor authentication logs")
    print(f"   • Set up key rotation schedule")

if __name__ == "__main__":
    main()
