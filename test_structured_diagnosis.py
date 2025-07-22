#!/usr/bin/env python3
"""Comprehensive test script for structured diagnosis endpoints."""

import json
import requests
from datetime import datetime
from jose import jwt
from app.config.settings import settings

def create_test_token():
    """Create a test JWT token."""
    from datetime import timedelta
    payload = {
        "sub": "test_user_123",
        "username": "test_user",
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token

def test_vaginal_discharge():
    """Test case for vaginal discharge with drug allergies."""
    return {
        "patient_profile": {
            "age": 29,
            "request_id": "test_discharge_001",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        },
        "primary_complaint": {
            "main_symptom": "vaginal_discharge",
            "duration": "1 week",
            "severity": "moderate",
            "onset": "sudden",
            "progression": "stable"
        },
        "symptom_specific_details": {
            "discharge_characteristics": {
                "color": "white",
                "consistency": "cottage_cheese",
                "odor": "none",
                "associated_itching": "severe"
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
                "menarche_age": 12,
                "cycle_frequency": 30,
                "period_duration": 4
            }
        },
        "associated_symptoms": {
            "pain": {
                "pelvic_pain": "mild",
                "vulvar_irritation": "severe"
            },
            "systemic": {
                "fatigue": "none",
                "nausea": False,
                "fever": False
            }
        },
        "medical_context": {
            "current_medications": [],
            "recent_medications": [],
            "medical_conditions": ["diabetes"],
            "previous_gynecological_issues": ["yeast infections"],
            "allergies": ["penicillin", "amoxicillin", "fluconazole"],
            "family_history": []
        },
        "healthcare_interaction": {
            "previous_consultation": True,
            "consultation_outcome": "inconclusive",
            "investigations_done": False,
            "current_treatment": "none"
        },
        "patient_concerns": {
            "main_worry": "recurrent infections",
            "impact_on_life": "moderate",
            "additional_notes": "I have multiple drug allergies and need safe alternatives"
        }
    }

def test_pelvic_pain():
    """Test case for severe pelvic pain."""
    return {
        "patient_profile": {
            "age": 25,
            "request_id": "test_pelvic_pain_002",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        },
        "primary_complaint": {
            "main_symptom": "pelvic_pain",
            "duration": "3 days",
            "severity": "severe",
            "onset": "sudden",
            "progression": "worsening"
        },
        "symptom_specific_details": {
            "bleeding_pattern": {
                "abnormal_bleeding": True,
                "flow_amount": "heavy",
                "timing": "between_periods"
            }
        },
        "reproductive_history": {
            "pregnancy_status": {
                "could_be_pregnant": True,
                "pregnancy_test_result": None
            },
            "sexual_activity": {
                "sexually_active": True,
                "last_intercourse": "1 week ago",
                "contraception_method": "none"
            },
            "menstrual_history": {
                "menarche_age": 13,
                "cycle_frequency": 28,
                "period_duration": 5
            }
        },
        "associated_symptoms": {
            "pain": {
                "pelvic_pain": "severe",
                "back_pain": "moderate",
                "cramping": "severe"
            },
            "systemic": {
                "fatigue": "moderate",
                "nausea": True,
                "fever": False
            }
        },
        "medical_context": {
            "current_medications": [],
            "recent_medications": [],
            "medical_conditions": [],
            "previous_gynecological_issues": [],
            "allergies": [],
            "family_history": []
        },
        "healthcare_interaction": {
            "previous_consultation": False,
            "investigations_done": False,
            "current_treatment": None
        },
        "patient_concerns": {
            "main_worry": "severe pain and unusual bleeding",
            "impact_on_life": "unable to work",
            "additional_notes": "Pain started suddenly and is getting worse"
        }
    }

def test_missed_period():
    """Test case for missed period with pregnancy concern."""
    return {
        "patient_profile": {
            "age": 22,
            "request_id": "test_missed_period_003",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        },
        "primary_complaint": {
            "main_symptom": "missed_period",
            "duration": "2 weeks",
            "severity": "moderate",
            "onset": "gradual",
            "progression": "stable"
        },
        "symptom_specific_details": {
            "cycle_context": {
                "usual_cycle_length": 28,
                "days_late": 14
            }
        },
        "reproductive_history": {
            "pregnancy_status": {
                "could_be_pregnant": True,
                "pregnancy_test_result": None
            },
            "sexual_activity": {
                "sexually_active": True,
                "last_intercourse": "3 weeks ago",
                "contraception_method": "birth_control_pills"
            },
            "menstrual_history": {
                "menarche_age": 12,
                "cycle_frequency": 28,
                "period_duration": 5
            }
        },
        "associated_symptoms": {
            "pain": {
                "pelvic_pain": "none"
            },
            "systemic": {
                "fatigue": "mild",
                "nausea": True,
                "fever": False
            }
        },
        "medical_context": {
            "current_medications": ["birth control pills"],
            "recent_medications": [],
            "medical_conditions": [],
            "previous_gynecological_issues": [],
            "allergies": [],
            "family_history": []
        },
        "healthcare_interaction": {
            "previous_consultation": False,
            "investigations_done": False,
            "current_treatment": None
        },
        "patient_concerns": {
            "main_worry": "possible pregnancy",
            "impact_on_life": "anxiety about results",
            "additional_notes": "Taking birth control but missed some pills"
        }
    }

def run_tests():
    """Run all structured diagnosis tests."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Tenderly AI Agent - Structured Diagnosis Endpoints")
    print("=" * 70)
    
    # Test cases
    test_cases = [
        ("Vaginal Discharge with Allergies", test_vaginal_discharge()),
        ("Severe Pelvic Pain", test_pelvic_pain()),
        ("Missed Period", test_missed_period()),
    ]
    
    for test_name, test_data in test_cases:
        print(f"\n📋 Testing: {test_name}")
        print("-" * 50)
        
        # Test the unauthenticated test endpoint
        print("1. Testing /structured/test endpoint (no auth required)...")
        try:
            response = requests.post(
                f"{base_url}/api/v1/diagnosis/structured/test",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Test endpoint successful!")
                print(f"   Request ID: {result.get('request_id')}")
                print(f"   Primary diagnosis: {result['possible_diagnoses'][0]['name'] if result.get('possible_diagnoses') else 'N/A'}")
                print(f"   Confidence: {result.get('confidence_score', 'N/A')}")
                print(f"   Urgency: {result.get('risk_assessment', {}).get('urgency_level', 'N/A')}")
                print(f"   Safe medications: {len(result.get('treatment_recommendations', {}).get('safe_medications', []))}")
            else:
                print(f"❌ Test endpoint failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            
        # Test the authenticated endpoint
        print("\n2. Testing /structured endpoint (auth required)...")
        try:
            token = create_test_token()
            response = requests.post(
                f"{base_url}/api/v1/diagnosis/structured",
                json=test_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Authenticated endpoint successful!")
                print(f"   Request ID: {result.get('request_id')}")
                print(f"   Primary diagnosis: {result['possible_diagnoses'][0]['name'] if result.get('possible_diagnoses') else 'N/A'}")
                print(f"   Confidence: {result.get('confidence_score', 'N/A')}")
            else:
                print(f"❌ Authenticated endpoint failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except Exception as e:
            print(f"❌ Token creation failed: {e}")
    
    print(f"\n{'=' * 70}")
    print("✅ Structured diagnosis testing complete!")
    print("\n📝 Note: The structured diagnosis endpoints provide comprehensive")
    print("   medical assessments with allergy considerations and safety warnings.")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"❌ Testing failed: {e}")
