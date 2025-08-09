#!/usr/bin/env python3
"""Test script to call the AI agent API with a valid JWT token."""

import requests
import json
from datetime import datetime
from jose import jwt

# JWT configuration (same as backend)
JWT_SECRET_KEY = "shared-jwt-secret-key-for-ai-agent"
JWT_ALGORITHM = "HS256"

def create_test_token():
    """Create a test JWT token like the backend would."""
    now = int(datetime.now().timestamp())
    expires_in = 3600  # 1 hour
    
    payload = {
        "sub": "tenderly-backend-service",
        "username": "backend-service",
        "exp": now + expires_in,
        "iat": now,
        "aud": "ai-diagnosis-service",
        "iss": "tenderly-backend",
        "service": True,
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def test_api_endpoint():
    """Test the API endpoint that was failing."""
    # Create a valid JWT token
    token = create_test_token()
    print(f"Created JWT token: {token[:50]}...")
    
    # API endpoint URL
    url = "http://localhost:8000/api/v1/diagnosis/structure"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Service-Name": "tenderly-backend",
        "X-Request-ID": "test-request-123",
        "X-Session-ID": "test-session-456"
    }
    
    # Sample request payload (simplified)
    payload = {
        "patient_profile": {
            "age": 28,
            "request_id": "test-patient-123",
            "timestamp": datetime.now().isoformat() + "Z"
        },
        "primary_complaint": {
            "main_symptom": "vaginal_discharge_with_itching",
            "duration": "3 days",
            "severity": "moderate",
            "onset": "gradual",
            "progression": "worsening"
        },
        "symptom_specific_details": {
            "symptom_characteristics": {
                "discharge_color": "white",
                "discharge_consistency": "thick",
                "odor": "none",
                "itching_severity": "severe"
            }
        },
        "reproductive_history": {
            "pregnancy_status": {
                "could_be_pregnant": False,
                "pregnancy_test_result": "negative"
            },
            "sexual_activity": {
                "sexually_active": True,
                "contraception_method": "condoms"
            },
            "menstrual_history": {
                "menarche_age": 13,
                "cycle_frequency": 28,
                "period_duration": 5
            }
        },
        "associated_symptoms": {
            "pain": {
                "pelvic_pain": "none",
                "vulvar_irritation": "moderate"
            },
            "systemic": {
                "fatigue": "mild",
                "nausea": False,
                "fever": False
            }
        },
        "medical_context": {
            "current_medications": [],
            "recent_medications": ["antibiotics"],
            "medical_conditions": ["diabetes_type_2"],
            "previous_gynecological_issues": [],
            "allergies": ["fluconazole"],
            "family_history": ["diabetes"]
        },
        "healthcare_interaction": {
            "previous_consultation": False,
            "consultation_outcome": "none",
            "investigations_done": False,
            "current_treatment": "none"
        },
        "patient_concerns": {
            "main_worry": "Recurrent yeast infections",
            "impact_on_life": "moderate",
            "additional_notes": "Concerned about diabetes affecting infections"
        }
    }
    
    print(f"Making POST request to: {url}")
    print("Headers:", json.dumps({k: v for k, v in headers.items() if k != "Authorization"}, indent=2))
    print("Authorization: Bearer [JWT_TOKEN]")
    print()
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! API call worked!")
            print("Response preview:")
            response_data = response.json()
            print(json.dumps({
                "request_id": response_data.get("request_id"),
                "patient_age": response_data.get("patient_age"),
                "primary_symptom": response_data.get("primary_symptom"),
                "confidence_score": response_data.get("confidence_score"),
                "diagnosis_count": len(response_data.get("possible_diagnoses", [])),
            }, indent=2))
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print("Response body:")
            try:
                print(json.dumps(response.json(), indent=2))
            except:
                print(response.text)
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the AI agent server running on localhost:8000?")
        print("Start it with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("=== AI Agent API Test ===")
    print()
    test_api_endpoint()
