"""Tests for the diagnosis endpoint."""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from jose import jwt
from app.main import app
from app.config.settings import settings

client = TestClient(app)


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


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Tenderly AI Agent" in response.json()["message"]


def test_health_endpoint():
    """Test the health endpoint."""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


def test_diagnosis_endpoint_without_auth():
    """Test diagnosis endpoint without authentication."""
    response = client.post(
        "/api/v1/diagnosis/",
        json={
            "diagnosis_request": {
                "symptoms": ["vaginal discharge", "itching"],
                "patient_age": 25,
                "severity_level": "moderate",
                "duration": "3 days"
            }
        }
    )
    assert response.status_code == 403  # Forbidden


def test_diagnosis_validation():
    """Test diagnosis request validation with authentication."""
    token = create_test_token()
    # Test with invalid age
    response = client.post(
        "/api/v1/diagnosis/",
        json={
            "diagnosis_request": {
                "symptoms": ["vaginal discharge"],
                "patient_age": 5,  # Invalid age
                "severity_level": "moderate",
                "duration": "3 days"
            }
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # Validation error


def test_symptom_validation():
    """Test symptom validation with authentication."""
    token = create_test_token()
    # Test with empty symptoms
    response = client.post(
        "/api/v1/diagnosis/",
        json={
            "diagnosis_request": {
                "symptoms": [],  # Empty symptoms
                "patient_age": 25,
                "severity_level": "moderate",
                "duration": "3 days"
            }
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # Validation error


def test_successful_diagnosis():
    """Test successful diagnosis with valid request."""
    token = create_test_token()
    # Test with valid data
    response = client.post(
        "/api/v1/diagnosis/",
        json={
            "diagnosis_request": {
                "symptoms": ["vaginal discharge", "itching"],
                "patient_age": 25,
                "severity_level": "moderate",
                "duration": "3 days"
            }
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    result = response.json()
    assert "diagnosis" in result
    assert "confidence_score" in result
    assert "recommended_medications" in result
    assert isinstance(result["recommended_medications"], list)
    assert "disclaimer" in result


if __name__ == "__main__":
    pytest.main([__file__])
