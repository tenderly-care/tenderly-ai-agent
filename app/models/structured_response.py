"""Structured response models for advanced AI diagnosis output."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from .response import Medication, Investigation, PossibleDiagnosis

class AllergyConsideration(BaseModel):
    """Model for allergy considerations in treatment."""
    
    allergic_medications: List[str] = Field(default_factory=list, description="Medications patient is allergic to")
    safe_alternatives: List[str] = Field(default_factory=list, description="Safe alternative medications")
    contraindicated_drugs: List[str] = Field(default_factory=list, description="Drugs to avoid")

class SafetyAssessment(BaseModel):
    """Model for safety assessment based on patient allergies and conditions."""
    
    allergy_considerations: AllergyConsideration = Field(..., description="Allergy-related safety considerations")
    condition_interactions: List[str] = Field(default_factory=list, description="Interactions with existing conditions")
    safety_warnings: List[str] = Field(default_factory=list, description="Important safety warnings")

class TreatmentRecommendation(BaseModel):
    """Model for comprehensive treatment recommendations."""
    
    primary_treatment: Optional[str] = Field(None, description="Primary recommended treatment")
    safe_medications: List[Medication] = Field(default_factory=list, description="Safe medications considering allergies")
    lifestyle_modifications: List[str] = Field(default_factory=list, description="Lifestyle modification recommendations")
    dietary_advice: List[str] = Field(default_factory=list, description="Dietary recommendations")
    follow_up_timeline: str = Field(..., description="Recommended follow-up timeline")

class RiskAssessment(BaseModel):
    """Model for risk assessment."""
    
    urgency_level: str = Field(..., description="Urgency level (low, moderate, high, urgent)")
    red_flags: List[str] = Field(default_factory=list, description="Red flag symptoms to watch for")
    when_to_seek_emergency_care: List[str] = Field(default_factory=list, description="When to seek emergency care")

class StructuredDiagnosisResponse(BaseModel):
    """Comprehensive response model for structured diagnosis endpoint."""
    
    # Request tracking
    request_id: str = Field(..., description="Original request ID")
    patient_age: int = Field(..., description="Patient age")
    primary_symptom: str = Field(..., description="Primary symptom analyzed")
    
    # Diagnosis results
    possible_diagnoses: List[PossibleDiagnosis] = Field(
        ...,
        description="List of possible diagnoses with confidence scores",
        min_items=1,
        max_items=3
    )
    
    # Clinical assessment
    clinical_reasoning: str = Field(..., description="Clinical reasoning behind the diagnosis")
    differential_considerations: List[str] = Field(default_factory=list, description="Differential diagnosis considerations")
    
    # Safety and risk assessment
    safety_assessment: SafetyAssessment = Field(..., description="Safety assessment based on allergies and conditions")
    risk_assessment: RiskAssessment = Field(..., description="Risk and urgency assessment")
    
    # Investigations and tests
    recommended_investigations: List[Investigation] = Field(
        default_factory=list,
        description="Recommended investigations and tests"
    )
    
    # Treatment recommendations
    treatment_recommendations: TreatmentRecommendation = Field(..., description="Comprehensive treatment recommendations")
    
    # Patient education
    patient_education: List[str] = Field(default_factory=list, description="Patient education points")
    warning_signs: List[str] = Field(default_factory=list, description="Warning signs to watch for")
    
    # Metadata
    confidence_score: float = Field(
        ...,
        description="Overall confidence score (0.0 - 1.0)",
        ge=0.0,
        le=1.0
    )
    
    processing_notes: List[str] = Field(default_factory=list, description="Processing notes and considerations")
    
    disclaimer: str = Field(..., description="Medical disclaimer")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "request_id": "req_allergy_002",
                "patient_age": 29,
                "primary_symptom": "vaginal_discharge",
                "possible_diagnoses": [
                    {
                        "name": "Vaginal Candidiasis (Yeast Infection)",
                        "confidence_score": 0.87,
                        "description": "Fungal infection characterized by white cottage cheese-like discharge with severe itching"
                    },
                    {
                        "name": "Bacterial Vaginosis",
                        "confidence_score": 0.23,
                        "description": "Less likely given the absence of fishy odor and cottage cheese consistency"
                    }
                ],
                "clinical_reasoning": "The combination of white cottage cheese-like discharge with no odor and severe itching strongly suggests vaginal candidiasis. Patient's history of diabetes increases susceptibility to yeast infections.",
                "differential_considerations": [
                    "Bacterial vaginosis ruled out due to lack of fishy odor",
                    "Trichomoniasis less likely given discharge characteristics"
                ],
                "safety_assessment": {
                    "allergy_considerations": {
                        "allergic_medications": ["fluconazole", "penicillin", "amoxicillin", "sulfa drugs", "bactrim"],
                        "safe_alternatives": ["topical antifungals", "nystatin", "terconazole"],
                        "contraindicated_drugs": ["fluconazole", "all penicillin-based antibiotics"]
                    },
                    "condition_interactions": ["diabetes may increase infection recurrence"],
                    "safety_warnings": ["Avoid all listed allergenic medications", "Monitor blood sugar levels"]
                },
                "risk_assessment": {
                    "urgency_level": "low",
                    "red_flags": ["fever", "severe abdominal pain", "blood in discharge"],
                    "when_to_seek_emergency_care": ["High fever with chills", "Severe pelvic pain"]
                },
                "recommended_investigations": [
                    {
                        "name": "Vaginal pH test",
                        "priority": "medium",
                        "reason": "To confirm yeast infection vs bacterial vaginosis"
                    },
                    {
                        "name": "KOH wet mount",
                        "priority": "high",
                        "reason": "To visualize yeast cells and confirm diagnosis"
                    }
                ],
                "treatment_recommendations": {
                    "primary_treatment": "Topical antifungal therapy due to fluconazole allergy",
                    "safe_medications": [
                        {
                            "name": "Miconazole (topical)",
                            "dosage": "2% cream",
                            "frequency": "Twice daily",
                            "duration": "7 days",
                            "reason": "Safe alternative to oral fluconazole",
                            "notes": "Apply intravaginally"
                        }
                    ],
                    "lifestyle_modifications": [
                        "Wear breathable cotton underwear",
                        "Avoid tight-fitting clothes",
                        "Maintain good blood sugar control"
                    ],
                    "dietary_advice": [
                        "Reduce sugar intake to help manage diabetes and prevent recurrence",
                        "Consider probiotic-rich foods"
                    ],
                    "follow_up_timeline": "1-2 weeks if symptoms persist"
                },
                "patient_education": [
                    "Yeast infections are common in people with diabetes",
                    "Complete the full course of treatment even if symptoms improve",
                    "Avoid douching or scented feminine products"
                ],
                "warning_signs": [
                    "Worsening symptoms after 3 days of treatment",
                    "Development of fever or severe pain",
                    "Recurrent infections (>4 per year)"
                ],
                "confidence_score": 0.87,
                "processing_notes": [
                    "Multiple drug allergies required careful medication selection",
                    "Diabetes increases risk of recurrent yeast infections"
                ],
                "disclaimer": "This AI-generated diagnosis should not replace professional medical consultation. Please consult a healthcare provider for proper evaluation and treatment.",
                "timestamp": "2025-07-19T05:06:30Z"
            }
        }
