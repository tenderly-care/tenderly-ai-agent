"""Tests for the diagnosis endpoint."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


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
            "symptoms": ["vaginal discharge", "itching"],
            "patient_age": 25,
            "severity_level": "moderate",
            "duration": "3 days"
        }
    )
    assert response.status_code == 401  # Unauthorized


def test_diagnosis_validation():
    """Test diagnosis request validation."""
    # Test with invalid age
    response = client.post(
        "/api/v1/diagnosis/",
        json={
            "symptoms": ["vaginal discharge"],
            "patient_age": 5,  # Invalid age
            "severity_level": "moderate",
            "duration": "3 days"
        }
    )
    assert response.status_code == 401  # Will be 422 after auth is bypassed


def test_symptom_validation():
    """Test symptom validation."""
    # Test with empty symptoms
    response = client.post(
        "/api/v1/diagnosis/",
        json={
            "symptoms": [],  # Empty symptoms
            "patient_age": 25,
            "severity_level": "moderate",
            "duration": "3 days"
        }
    )
    assert response.status_code == 401  # Will be 422 after auth is bypassed


if __name__ == "__main__":
    pytest.main([__file__])
