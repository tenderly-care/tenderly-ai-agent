"""Request models for the AI diagnosis API."""

from typing import List, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum


class SeverityLevel(str, Enum):
    """Severity levels for symptoms."""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class OnsetType(str, Enum):
    """Onset types for symptoms."""
    SUDDEN = "sudden"
    GRADUAL = "gradual"
    CHRONIC = "chronic"


class ProgressionType(str, Enum):
    """Progression types for symptoms."""
    STABLE = "stable"
    IMPROVING = "improving"
    WORSENING = "worsening"
    FLUCTUATING = "fluctuating"


class DiagnosisRequest(BaseModel):
    """Request model for diagnosis endpoint."""
    
    symptoms: List[str] = Field(
        ...,
        description="List of symptoms reported by the patient",
        min_items=1,
        max_items=3,
        example=["vaginal discharge", "itching", "burning sensation"]
    )
    
    patient_age: int = Field(
        ...,
        description="Patient's age in years",
        ge=12,
        le=100,
        example=25
    )
    
    severity_level: SeverityLevel = Field(
        SeverityLevel.MODERATE,
        description="Severity level of symptoms"
    )
    
    duration: str = Field(
        ...,
        description="Duration of symptoms",
        max_length=50,
        example="3 days"
    )
    
    onset: Optional[OnsetType] = Field(
        None,
        description="Onset type of symptoms",
        example="sudden"
    )
    
    progression: Optional[ProgressionType] = Field(
        None,
        description="Progression of symptoms over time",
        example="stable"
    )

    @validator("symptoms")
    def validate_symptoms(cls, v):
        """Validate symptoms list."""
        if not v:
            raise ValueError("At least one symptom is required")
        
        # Clean and validate each symptom
        cleaned_symptoms = []
        for symptom in v:
            if not isinstance(symptom, str):
                raise ValueError("Each symptom must be a string")
            
            cleaned_symptom = symptom.strip().lower()
            if len(cleaned_symptom) < 2:
                raise ValueError("Each symptom must be at least 2 characters long")
            if len(cleaned_symptom) > 100:
                raise ValueError("Each symptom must be less than 100 characters")
            
            cleaned_symptoms.append(cleaned_symptom)
        
        return cleaned_symptoms

    @validator("duration")
    def validate_duration(cls, v):
        """Validate duration format."""
        if not v or not v.strip():
            raise ValueError("Duration is required")
        
        duration = v.strip().lower()
        if len(duration) < 1:
            raise ValueError("Duration cannot be empty")
        
        return duration

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "symptoms": ["vaginal discharge", "itching", "burning sensation"],
                "patient_age": 25,
                "severity_level": "moderate",
                "duration": "3 days",
                "onset": "sudden",
                "progression": "stable"
            }
        }


class SymptomValidationRequest(BaseModel):
    """Request model for symptom validation."""
    
    symptoms: List[str] = Field(
        ...,
        description="List of symptoms to validate",
        min_items=1,
        max_items=20
    )

    @validator("symptoms")
    def validate_symptoms(cls, v):
        """Validate symptoms list."""
        return DiagnosisRequest.validate_symptoms(v)
