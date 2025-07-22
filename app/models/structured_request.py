"""Structured request models for advanced AI diagnosis input."""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime

class SeverityLevel(str, Enum):
    NONE = "none"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"

class MainSymptom(str, Enum):
    EXCESSIVE_VAGINAL_BLEEDING = "excessive_vaginal_bleeding"
    VAGINAL_DISCHARGE = "vaginal_discharge"
    PELVIC_PAIN = "pelvic_pain"
    MISSED_PERIOD = "missed_period"
    PAINFUL_PERIODS = "painful_periods"

class OnsetType(str, Enum):
    SUDDEN = "sudden"
    GRADUAL = "gradual"
    CHRONIC = "chronic"

class ProgressionType(str, Enum):
    STABLE = "stable"
    IMPROVING = "improving"
    WORSENING = "worsening"
    FLUCTUATING = "fluctuating"

class PatientProfile(BaseModel):
    age: int = Field(..., description="Patient's age", ge=10, le=100)
    request_id: str = Field(..., description="Unique request identifier")
    timestamp: str = Field(..., description="Request timestamp in ISO format")

class PrimaryComplaint(BaseModel):
    main_symptom: MainSymptom = Field(..., description="Primary symptom")
    duration: str = Field(..., description="Duration of symptoms")
    severity: SeverityLevel = Field(..., description="Severity level")
    onset: OnsetType = Field(..., description="Onset type")
    progression: ProgressionType = Field(..., description="Symptom progression")

class DischargeCharacteristics(BaseModel):
    color: str = Field(..., description="Discharge color")
    consistency: str = Field(..., description="Discharge consistency")
    odor: str = Field(..., description="Discharge odor")
    associated_itching: SeverityLevel = Field(..., description="Associated itching severity")

class SymptomSpecificDetails(BaseModel):
    discharge_characteristics: Optional[DischargeCharacteristics] = Field(None, description="Discharge details for vaginal discharge symptoms")
    bleeding_pattern: Optional[Dict[str, Any]] = Field(None, description="Bleeding pattern for bleeding symptoms")
    cycle_context: Optional[Dict[str, Any]] = Field(None, description="Menstrual cycle context")

class PregnancyStatus(BaseModel):
    could_be_pregnant: bool = Field(..., description="Possibility of pregnancy")
    pregnancy_test_result: Optional[str] = Field(None, description="Pregnancy test result")
    test_date: Optional[str] = Field(None, description="Date of pregnancy test")

class SexualActivity(BaseModel):
    sexually_active: bool = Field(..., description="Sexual activity status")
    last_intercourse: Optional[str] = Field(None, description="Date of last intercourse")
    contraception_method: Optional[str] = Field(None, description="Contraception method used")
    contraceptive_pills: Optional[str] = Field(None, description="Contraceptive pills used")

class MenstrualHistory(BaseModel):
    menarche_age: int = Field(..., description="Age at menarche", ge=8, le=18)
    cycle_frequency: int = Field(..., description="Cycle frequency in days", ge=21, le=35)
    period_duration: int = Field(..., description="Period duration in days", ge=2, le=10)
    flow_volume: Optional[str] = Field(None, description="Flow volume")
    dysmenorrhea: Optional[SeverityLevel] = Field(None, description="Painful periods severity")
    clots_normal: Optional[bool] = Field(None, description="Normal clots presence")

class ReproductiveHistory(BaseModel):
    pregnancy_status: PregnancyStatus = Field(..., description="Pregnancy status details")
    sexual_activity: SexualActivity = Field(..., description="Sexual activity details")
    menstrual_history: MenstrualHistory = Field(..., description="Menstrual history")

class PainSymptoms(BaseModel):
    pelvic_pain: SeverityLevel = Field(..., description="Pelvic pain severity")
    back_pain: Optional[SeverityLevel] = Field(None, description="Back pain severity")
    cramping: Optional[SeverityLevel] = Field(None, description="Cramping severity")
    pain_timing: Optional[str] = Field(None, description="Pain timing")
    vulvar_irritation: Optional[SeverityLevel] = Field(None, description="Vulvar irritation severity")

class SystemicSymptoms(BaseModel):
    fatigue: Union[SeverityLevel, str] = Field(..., description="Fatigue level (can be severity level or 'none')")
    dizziness: Optional[SeverityLevel] = Field(None, description="Dizziness severity")
    nausea: bool = Field(..., description="Nausea presence")
    fever: bool = Field(..., description="Fever presence")
    weight_change: Optional[str] = Field(None, description="Weight change")
    
    @validator('fatigue')
    def validate_fatigue(cls, v):
        """Validate fatigue field to accept both severity levels and 'none'."""
        if isinstance(v, str):
            valid_values = ['none', 'mild', 'moderate', 'severe']
            if v.lower() not in valid_values:
                raise ValueError(f"Fatigue must be one of {valid_values}")
            return v.lower()
        return v

class AssociatedSymptoms(BaseModel):
    pain: PainSymptoms = Field(..., description="Pain-related symptoms")
    systemic: SystemicSymptoms = Field(..., description="Systemic symptoms")

class MedicalContext(BaseModel):
    current_medications: List[str] = Field(default_factory=list, description="Current medications")
    recent_medications: List[str] = Field(default_factory=list, description="Recent medications")
    medical_conditions: List[str] = Field(default_factory=list, description="Medical conditions")
    previous_gynecological_issues: List[str] = Field(default_factory=list, description="Previous gynecological issues")
    allergies: List[str] = Field(default_factory=list, description="Drug allergies")
    family_history: List[str] = Field(default_factory=list, description="Family medical history")

class HealthcareInteraction(BaseModel):
    previous_consultation: bool = Field(..., description="Previous consultation status")
    consultation_outcome: Optional[str] = Field(None, description="Previous consultation outcome")
    investigations_done: bool = Field(..., description="Investigations done status")
    investigation_results: Optional[str] = Field(None, description="Investigation results")
    current_treatment: Optional[str] = Field(None, description="Current treatment")

class PatientConcerns(BaseModel):
    main_worry: str = Field(..., description="Patient's main worry")
    impact_on_life: str = Field(..., description="Impact on patient's life")
    additional_notes: Optional[str] = Field(None, description="Additional notes from patient")

class StructuredDiagnosisRequest(BaseModel):
    patient_profile: PatientProfile = Field(..., description="Patient profile information")
    primary_complaint: PrimaryComplaint = Field(..., description="Primary complaint details")
    symptom_specific_details: SymptomSpecificDetails = Field(..., description="Symptom-specific details")
    reproductive_history: ReproductiveHistory = Field(..., description="Reproductive history")
    associated_symptoms: AssociatedSymptoms = Field(..., description="Associated symptoms")
    medical_context: MedicalContext = Field(..., description="Medical context")
    healthcare_interaction: HealthcareInteraction = Field(..., description="Healthcare interaction history")
    patient_concerns: PatientConcerns = Field(..., description="Patient concerns and notes")
    
    @validator('symptom_specific_details')
    def validate_symptom_specific_details(cls, v, values):
        """Validate symptom-specific details based on main symptom."""
        if 'primary_complaint' in values:
            main_symptom = values['primary_complaint'].main_symptom
            if main_symptom == MainSymptom.VAGINAL_DISCHARGE:
                if not v.discharge_characteristics:
                    raise ValueError("Discharge characteristics are required for vaginal discharge symptoms")
            elif main_symptom == MainSymptom.EXCESSIVE_VAGINAL_BLEEDING:
                if not v.bleeding_pattern:
                    raise ValueError("Bleeding pattern details are required for bleeding symptoms")
        return v
    
    @validator('patient_profile')
    def validate_patient_profile(cls, v):
        """Additional validation for patient profile."""
        # Validate timestamp format
        try:
            datetime.fromisoformat(v.timestamp.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError("Timestamp must be in valid ISO format (e.g., 2025-07-21T06:03:52Z)")
        
        # Validate request ID format
        if not v.request_id or len(v.request_id.strip()) < 3:
            raise ValueError("Request ID must be at least 3 characters long")
            
        return v
    
    @validator('medical_context')
    def validate_medical_context(cls, v):
        """Validate medical context for safety."""
        # Check for potential medication conflicts
        all_medications = v.current_medications + v.recent_medications
        if v.allergies:
            for med in all_medications:
                for allergy in v.allergies:
                    if allergy.lower() in med.lower():
                        raise ValueError(f"Medication '{med}' conflicts with reported allergy to '{allergy}'")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "patient_profile": {
                    "age": 29,
                    "request_id": "req_allergy_002",
                    "timestamp": "2025-07-19T05:06:30Z"
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
                        "fever": False
                    }
                },
                "medical_context": {
                    "current_medications": [],
                    "recent_medications": [],
                    "medical_conditions": ["diabetes"],
                    "previous_gynecological_issues": ["yeast infections"],
                    "allergies": [
                        "penicillin",
                        "amoxicillin", 
                        "sulfa drugs",
                        "bactrim",
                        "fluconazole"
                    ],
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
                    "additional_notes": "I have many drug allergies and need safe alternatives"
                }
            }
        }

