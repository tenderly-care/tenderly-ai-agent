"""Response models for the AI diagnosis API."""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Medication(BaseModel):
    """Medication recommendation model."""
    
    name: str = Field(..., description="Medication name")
    dosage: str = Field(..., description="Dosage amount")
    frequency: str = Field(..., description="How often to take")
    duration: str = Field(..., description="Duration of treatment")
    reason: str = Field(..., description="Reason for prescribing this medication")
    notes: Optional[str] = Field(None, description="Additional notes")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "Fluconazole",
                "dosage": "150mg",
                "frequency": "Once daily",
                "duration": "1 day",
                "reason": "To treat vaginal yeast infection",
                "notes": "Take with food"
            }
        }


class Investigation(BaseModel):
    """Medical investigation recommendation model."""
    
    name: str = Field(..., description="Investigation name")
    priority: str = Field(..., description="Priority level (low, medium, high)")
    reason: str = Field(..., description="Reason for investigation")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "Vaginal swab culture",
                "priority": "medium",
                "reason": "To identify specific pathogen"
            }
        }


class PossibleDiagnosis(BaseModel):
    """Possible diagnosis with confidence score."""
    
    name: str = Field(..., description="Diagnosis name")
    confidence_score: float = Field(
        ...,
        description="Confidence score (0.0 - 1.0)",
        ge=0.0,
        le=1.0
    )
    description: Optional[str] = Field(None, description="Brief diagnosis description")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "Vaginal Candidiasis",
                "confidence_score": 0.85,
                "description": "Fungal infection of the vagina"
            }
        }


class ConciseDiagnosisResponse(BaseModel):
    """Concise response model for diagnosis endpoint with 1-2 probable diagnoses."""
    
    possible_diagnoses: List[PossibleDiagnosis] = Field(
        ...,
        description="List of 1-2 most probable diagnoses with confidence scores",
        min_items=1,
        max_items=2
    )
    
    suggested_investigations: List[Investigation] = Field(
        default_factory=list,
        description="Recommended medical investigations"
    )
    
    disclaimer: str = Field(
        ...,
        description="Medical disclaimer"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "possible_diagnoses": [
                    {
                        "name": "Vaginal Candidiasis",
                        "confidence_score": 0.85,
                        "description": "Fungal infection of the vagina"
                    },
                    {
                        "name": "Bacterial Vaginosis",
                        "confidence_score": 0.72,
                        "description": "Bacterial imbalance in vaginal flora"
                    }
                ],
                "suggested_investigations": [
                    {
                        "name": "Vaginal pH test",
                        "priority": "medium",
                        "reason": "To differentiate between yeast and bacterial infections"
                    },
                    {
                        "name": "Microscopic examination",
                        "priority": "high",
                        "reason": "To confirm diagnosis and identify pathogen"
                    }
                ],
                "disclaimer": "This is an AI-generated diagnosis and should not replace professional medical consultation.",
                "timestamp": "2023-11-15T10:30:00Z"
            }
        }


class DiagnosisResponse(BaseModel):
    """Response model for diagnosis endpoint."""
    
    diagnosis: str = Field(..., description="Primary diagnosis")
    
    confidence_score: float = Field(
        ...,
        description="Confidence score (0.0 - 1.0)",
        ge=0.0,
        le=1.0
    )
    
    suggested_investigations: List[Investigation] = Field(
        default_factory=list,
        description="Recommended medical investigations"
    )
    
    recommended_medications: List[Medication] = Field(
        default_factory=list,
        description="Recommended medications"
    )
    
    lifestyle_advice: List[str] = Field(
        default_factory=list,
        description="Lifestyle recommendations"
    )
    
    follow_up_recommendations: str = Field(
        ...,
        description="Follow-up recommendations"
    )
    
    disclaimer: str = Field(
        ...,
        description="Medical disclaimer"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "diagnosis": "Vaginal Candidiasis (Yeast Infection)",
                "confidence_score": 0.85,
                "suggested_investigations": [
                    {
                        "name": "Vaginal pH test",
                        "priority": "medium",
                        "reason": "To confirm diagnosis"
                    }
                ],
                "recommended_medications": [
                    {
                        "name": "Fluconazole",
                        "dosage": "150mg",
                        "frequency": "Once",
                        "duration": "Single dose",
                        "reason": "To treat vaginal yeast infection",
                        "notes": "Oral antifungal medication"
                    }
                ],
                "lifestyle_advice": [
                    "Wear breathable cotton underwear",
                    "Avoid tight-fitting clothes",
                    "Maintain good hygiene"
                ],
                "follow_up_recommendations": "Follow up in 1 week if symptoms persist",
                "disclaimer": "This is an AI-generated diagnosis and should not replace professional medical consultation.",
                "timestamp": "2023-11-15T10:30:00Z"
            }
        }


class SymptomValidationResponse(BaseModel):
    """Response model for symptom validation."""
    
    valid_symptoms: List[str] = Field(
        default_factory=list,
        description="List of valid symptoms"
    )
    
    invalid_symptoms: List[str] = Field(
        default_factory=list,
        description="List of invalid symptoms"
    )
    
    suggestions: List[str] = Field(
        default_factory=list,
        description="Suggested corrections for invalid symptoms"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "valid_symptoms": ["vaginal discharge", "itching"],
                "invalid_symptoms": ["xyz symptom"],
                "suggestions": ["vaginal burning", "pelvic pain"]
            }
        }


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(..., description="API version")
    
    services: dict = Field(
        default_factory=dict,
        description="External service status"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2023-11-15T10:30:00Z",
                "version": "1.0.0",
                "services": {
                    "openai": "healthy",
                    "redis": "healthy"
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "error": "Invalid input",
                "detail": "Symptoms list cannot be empty",
                "timestamp": "2023-11-15T10:30:00Z"
            }
        }
