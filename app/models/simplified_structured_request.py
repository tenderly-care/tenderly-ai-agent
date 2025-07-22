"""Simplified structured request models matching the new schema specification."""

from typing import List, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum


class SeverityLevel(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class PatientProfile(BaseModel):
    age: int = Field(..., description="Patient's age", ge=10, le=100)
    request_id: str = Field(..., description="Unique request identifier")
    timestamp: str = Field(..., description="Request timestamp in ISO format")


class PrimaryComplaint(BaseModel):
    main_symptom: str = Field(..., description="Primary symptom")
    duration: str = Field(..., description="Duration of symptoms")
    severity: SeverityLevel = Field(..., description="Severity level")
    onset: str = Field(..., description="Onset type")
    progression: str = Field(..., description="Symptom progression")


class SymptomSpecificDetails(BaseModel):
    symptom_characteristics: Dict[str, Union[str, int, bool, list, dict, None]] = Field(
        ..., description="Flexible symptom characteristics"
    )


class PregnancyStatus(BaseModel):
    could_be_pregnant: bool = Field(..., description="Possibility of pregnancy")
    pregnancy_test_result: str = Field(..., description="Pregnancy test result")


class SexualActivity(BaseModel):
    sexually_active: bool = Field(..., description="Sexual activity status")
    contraception_method: str = Field(..., description="Contraception method used")


class MenstrualHistory(BaseModel):
    menarche_age: int = Field(..., description="Age at menarche", ge=8, le=20)
    cycle_frequency: int = Field(..., description="Cycle frequency in days")
    period_duration: int = Field(..., description="Period duration in days")


class ReproductiveHistory(BaseModel):
    pregnancy_status: PregnancyStatus = Field(..., description="Pregnancy status details")
    sexual_activity: SexualActivity = Field(..., description="Sexual activity details")
    menstrual_history: MenstrualHistory = Field(..., description="Menstrual history")


class PainSymptoms(BaseModel):
    pelvic_pain: str = Field(default="", description="Pelvic pain severity")
    vulvar_irritation: str = Field(default="", description="Vulvar irritation severity")


class SystemicSymptoms(BaseModel):
    fatigue: str = Field(default="", description="Fatigue level")
    nausea: bool = Field(default=False, description="Nausea presence")
    fever: bool = Field(default=False, description="Fever presence")


class AssociatedSymptoms(BaseModel):
    pain: PainSymptoms = Field(..., description="Pain-related symptoms")
    systemic: SystemicSymptoms = Field(..., description="Systemic symptoms")


class MedicalContext(BaseModel):
    current_medications: List[str] = Field(..., description="Current medications")
    recent_medications: List[str] = Field(..., description="Recent medications")
    medical_conditions: List[str] = Field(..., description="Medical conditions")
    previous_gynecological_issues: List[str] = Field(..., description="Previous gynecological issues")
    allergies: List[str] = Field(..., description="Drug allergies")
    family_history: List[str] = Field(..., description="Family medical history")


class HealthcareInteraction(BaseModel):
    previous_consultation: bool = Field(..., description="Previous consultation status")
    consultation_outcome: str = Field(..., description="Previous consultation outcome")
    investigations_done: bool = Field(..., description="Investigations done status")
    current_treatment: str = Field(..., description="Current treatment")


class PatientConcerns(BaseModel):
    main_worry: str = Field(..., description="Patient's main worry")
    impact_on_life: str = Field(..., description="Impact on patient's life")
    additional_notes: str = Field(..., description="Additional notes from patient")


class SimplifiedStructuredDiagnosisRequest(BaseModel):
    """Simplified structured request matching the new schema."""
    
    patient_profile: PatientProfile = Field(..., description="Patient profile information")
    primary_complaint: PrimaryComplaint = Field(..., description="Primary complaint details")
    symptom_specific_details: SymptomSpecificDetails = Field(..., description="Symptom-specific details")
    reproductive_history: ReproductiveHistory = Field(..., description="Reproductive history")
    associated_symptoms: AssociatedSymptoms = Field(..., description="Associated symptoms")
    medical_context: MedicalContext = Field(..., description="Medical context")
    healthcare_interaction: HealthcareInteraction = Field(..., description="Healthcare interaction history")
    patient_concerns: PatientConcerns = Field(..., description="Patient concerns and notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_profile": {
                    "age": 25,
                    "request_id": "req_001",
                    "timestamp": "2025-07-22T10:51:50Z"
                },
                "primary_complaint": {
                    "main_symptom": "vaginal discharge",
                    "duration": "3 days",
                    "severity": "moderate",
                    "onset": "sudden",
                    "progression": "stable"
                },
                "symptom_specific_details": {
                    "symptom_characteristics": {
                        "color": "white",
                        "consistency": "cottage cheese",
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
                        "menarche_age": 12,
                        "cycle_frequency": 28,
                        "period_duration": 5
                    }
                },
                "associated_symptoms": {
                    "pain": {
                        "pelvic_pain": "mild",
                        "vulvar_irritation": "severe"
                    },
                    "systemic": {
                        "fatigue": "mild",
                        "nausea": False,
                        "fever": False
                    }
                },
                "medical_context": {
                    "current_medications": [],
                    "recent_medications": [],
                    "medical_conditions": ["diabetes"],
                    "previous_gynecological_issues": ["yeast infections"],
                    "allergies": ["penicillin", "fluconazole"],
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
                    "additional_notes": "I have multiple drug allergies"
                }
            }
        }
