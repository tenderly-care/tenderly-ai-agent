# 📋 Tenderly AI Agent - Complete JSON Schema Documentation

This document provides the complete JSON Schema definitions for all request and response models used by the Tenderly AI Agent API.

## 📚 Table of Contents

1. [Simple Diagnosis Endpoints](#simple-diagnosis-endpoints)
2. [Structured Diagnosis Endpoints](#structured-diagnosis-endpoints)
3. [Health Check Endpoints](#health-check-endpoints)
4. [Common Components](#common-components)
5. [Error Handling](#error-handling)

---

## 🔧 Simple Diagnosis Endpoints

### DiagnosisRequest Schema

**Endpoint:** `POST /api/v1/diagnosis/`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "title": "DiagnosisRequest",
  "description": "Request model for simple diagnosis endpoint",
  "required": ["symptoms", "patient_age", "duration"],
  "properties": {
    "symptoms": {
      "type": "array",
      "description": "List of symptoms reported by the patient",
      "items": { "type": "string" },
      "minItems": 1,
      "maxItems": 20,
      "example": ["vaginal discharge", "itching", "burning sensation"]
    },
    "patient_age": {
      "type": "integer",
      "description": "Patient's age in years",
      "minimum": 12,
      "maximum": 100,
      "example": 25
    },
    "medical_history": {
      "type": "array",
      "description": "Relevant medical history",
      "items": { "type": "string" },
      "maxItems": 10,
      "example": ["diabetes", "hypertension"]
    },
    "severity_level": {
      "type": "string",
      "enum": ["mild", "moderate", "severe"],
      "default": "moderate",
      "description": "Severity level of symptoms"
    },
    "duration": {
      "type": "string",
      "description": "Duration of symptoms",
      "maxLength": 50,
      "example": "3 days"
    },
    "onset": {
      "type": "string",
      "enum": ["sudden", "gradual", "chronic"],
      "description": "Onset type of symptoms",
      "example": "sudden"
    },
    "progression": {
      "type": "string",
      "enum": ["stable", "improving", "worsening", "fluctuating"],
      "description": "Progression of symptoms over time",
      "example": "stable"
    },
    "additional_notes": {
      "type": "string",
      "description": "Additional notes or context",
      "maxLength": 500
    }
  },
  "example": {
    "symptoms": ["vaginal discharge", "itching", "burning sensation"],
    "patient_age": 25,
    "medical_history": ["diabetes"],
    "severity_level": "moderate",
    "duration": "3 days",
    "onset": "sudden",
    "progression": "stable",
    "additional_notes": "Symptoms worsen at night"
  }
}
```

### DiagnosisResponse Schema

**Endpoint Response:** `POST /api/v1/diagnosis/`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "title": "DiagnosisResponse",
  "description": "Response model for simple diagnosis endpoint",
  "required": ["diagnosis", "confidence_score", "follow_up_recommendations", "disclaimer"],
  "properties": {
    "diagnosis": {
      "type": "string",
      "description": "Primary diagnosis"
    },
    "confidence_score": {
      "type": "number",
      "description": "Confidence score (0.0 - 1.0)",
      "minimum": 0.0,
      "maximum": 1.0
    },
    "suggested_investigations": {
      "type": "array",
      "description": "Recommended medical investigations",
      "items": { "$ref": "#/$defs/Investigation" }
    },
    "recommended_medications": {
      "type": "array",
      "description": "Recommended medications",
      "items": { "$ref": "#/$defs/Medication" }
    },
    "lifestyle_advice": {
      "type": "array",
      "description": "Lifestyle recommendations",
      "items": { "type": "string" }
    },
    "follow_up_recommendations": {
      "type": "string",
      "description": "Follow-up recommendations"
    },
    "disclaimer": {
      "type": "string",
      "description": "Medical disclaimer"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Response timestamp"
    }
  },
  "$defs": {
    "Investigation": {
      "type": "object",
      "required": ["name", "priority", "reason"],
      "properties": {
        "name": {
          "type": "string",
          "description": "Investigation name"
        },
        "priority": {
          "type": "string",
          "enum": ["low", "medium", "high"],
          "description": "Priority level"
        },
        "reason": {
          "type": "string",
          "description": "Reason for investigation"
        }
      }
    },
    "Medication": {
      "type": "object",
      "required": ["name", "dosage", "frequency", "duration", "reason"],
      "properties": {
        "name": {
          "type": "string",
          "description": "Medication name"
        },
        "dosage": {
          "type": "string",
          "description": "Dosage amount"
        },
        "frequency": {
          "type": "string",
          "description": "How often to take"
        },
        "duration": {
          "type": "string",
          "description": "Duration of treatment"
        },
        "reason": {
          "type": "string",
          "description": "Reason for prescribing"
        },
        "notes": {
          "type": "string",
          "description": "Additional notes"
        }
      }
    }
  }
}
```

---

## 🏥 Structured Diagnosis Endpoints

### StructuredDiagnosisRequest Schema

**Endpoint:** `POST /api/v1/diagnosis/structured`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "title": "StructuredDiagnosisRequest",
  "description": "Comprehensive structured request for detailed diagnosis",
  "required": [
    "patient_profile",
    "primary_complaint", 
    "symptom_specific_details",
    "reproductive_history",
    "associated_symptoms",
    "medical_context",
    "healthcare_interaction",
    "patient_concerns"
  ],
  "properties": {
    "patient_profile": {
      "$ref": "#/$defs/PatientProfile"
    },
    "primary_complaint": {
      "$ref": "#/$defs/PrimaryComplaint"
    },
    "symptom_specific_details": {
      "$ref": "#/$defs/SymptomSpecificDetails"
    },
    "reproductive_history": {
      "$ref": "#/$defs/ReproductiveHistory"
    },
    "associated_symptoms": {
      "$ref": "#/$defs/AssociatedSymptoms"
    },
    "medical_context": {
      "$ref": "#/$defs/MedicalContext"
    },
    "healthcare_interaction": {
      "$ref": "#/$defs/HealthcareInteraction"
    },
    "patient_concerns": {
      "$ref": "#/$defs/PatientConcerns"
    }
  },
  "$defs": {
    "PatientProfile": {
      "type": "object",
      "required": ["age", "request_id", "timestamp"],
      "properties": {
        "age": {
          "type": "integer",
          "minimum": 12,
          "maximum": 100,
          "description": "Patient's age"
        },
        "request_id": {
          "type": "string",
          "minLength": 3,
          "description": "Unique request identifier"
        },
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "Request timestamp in ISO format"
        }
      }
    },
    "PrimaryComplaint": {
      "type": "object",
      "required": ["main_symptom", "duration", "severity", "onset", "progression"],
      "properties": {
        "main_symptom": {
          "type": "string",
          "enum": [
            "excessive_vaginal_bleeding",
            "vaginal_discharge",
            "pelvic_pain",
            "missed_period",
            "painful_periods"
          ],
          "description": "Primary symptom"
        },
        "duration": {
          "type": "string",
          "description": "Duration of symptoms"
        },
        "severity": {
          "type": "string",
          "enum": ["none", "mild", "moderate", "severe"],
          "description": "Severity level"
        },
        "onset": {
          "type": "string",
          "enum": ["sudden", "gradual", "chronic"],
          "description": "Onset type"
        },
        "progression": {
          "type": "string",
          "enum": ["stable", "improving", "worsening", "fluctuating"],
          "description": "Symptom progression"
        }
      }
    },
    "SymptomSpecificDetails": {
      "type": "object",
      "properties": {
        "discharge_characteristics": {
          "$ref": "#/$defs/DischargeCharacteristics"
        },
        "bleeding_pattern": {
          "type": "object",
          "description": "Bleeding pattern details",
          "additionalProperties": true
        },
        "cycle_context": {
          "type": "object",
          "description": "Menstrual cycle context",
          "additionalProperties": true
        }
      }
    },
    "DischargeCharacteristics": {
      "type": "object",
      "required": ["color", "consistency", "odor", "associated_itching"],
      "properties": {
        "color": {
          "type": "string",
          "description": "Discharge color"
        },
        "consistency": {
          "type": "string",
          "description": "Discharge consistency"
        },
        "odor": {
          "type": "string",
          "description": "Discharge odor"
        },
        "associated_itching": {
          "type": "string",
          "enum": ["none", "mild", "moderate", "severe"],
          "description": "Associated itching severity"
        }
      }
    },
    "ReproductiveHistory": {
      "type": "object",
      "required": ["pregnancy_status", "sexual_activity", "menstrual_history"],
      "properties": {
        "pregnancy_status": {
          "$ref": "#/$defs/PregnancyStatus"
        },
        "sexual_activity": {
          "$ref": "#/$defs/SexualActivity"
        },
        "menstrual_history": {
          "$ref": "#/$defs/MenstrualHistory"
        }
      }
    },
    "PregnancyStatus": {
      "type": "object",
      "required": ["could_be_pregnant"],
      "properties": {
        "could_be_pregnant": {
          "type": "boolean",
          "description": "Possibility of pregnancy"
        },
        "pregnancy_test_result": {
          "type": "string",
          "description": "Pregnancy test result"
        },
        "test_date": {
          "type": "string",
          "format": "date",
          "description": "Date of pregnancy test"
        }
      }
    },
    "SexualActivity": {
      "type": "object",
      "required": ["sexually_active"],
      "properties": {
        "sexually_active": {
          "type": "boolean",
          "description": "Sexual activity status"
        },
        "last_intercourse": {
          "type": "string",
          "description": "Date of last intercourse"
        },
        "contraception_method": {
          "type": "string",
          "description": "Contraception method used"
        },
        "contraceptive_pills": {
          "type": "string",
          "description": "Contraceptive pills used"
        }
      }
    },
    "MenstrualHistory": {
      "type": "object",
      "required": ["menarche_age", "cycle_frequency", "period_duration"],
      "properties": {
        "menarche_age": {
          "type": "integer",
          "minimum": 8,
          "maximum": 18,
          "description": "Age at menarche"
        },
        "cycle_frequency": {
          "type": "integer",
          "minimum": 21,
          "maximum": 35,
          "description": "Cycle frequency in days"
        },
        "period_duration": {
          "type": "integer",
          "minimum": 2,
          "maximum": 10,
          "description": "Period duration in days"
        },
        "flow_volume": {
          "type": "string",
          "enum": ["light", "moderate", "heavy"],
          "description": "Flow volume"
        },
        "dysmenorrhea": {
          "type": "string",
          "enum": ["none", "mild", "moderate", "severe"],
          "description": "Painful periods severity"
        },
        "clots_normal": {
          "type": "boolean",
          "description": "Normal clots presence"
        }
      }
    },
    "AssociatedSymptoms": {
      "type": "object",
      "required": ["pain", "systemic"],
      "properties": {
        "pain": {
          "$ref": "#/$defs/PainSymptoms"
        },
        "systemic": {
          "$ref": "#/$defs/SystemicSymptoms"
        }
      }
    },
    "PainSymptoms": {
      "type": "object",
      "required": ["pelvic_pain"],
      "properties": {
        "pelvic_pain": {
          "type": "string",
          "enum": ["none", "mild", "moderate", "severe"],
          "description": "Pelvic pain severity"
        },
        "back_pain": {
          "type": "string",
          "enum": ["none", "mild", "moderate", "severe"],
          "description": "Back pain severity"
        },
        "cramping": {
          "type": "string",
          "enum": ["none", "mild", "moderate", "severe"],
          "description": "Cramping severity"
        },
        "pain_timing": {
          "type": "string",
          "description": "Pain timing"
        },
        "vulvar_irritation": {
          "type": "string",
          "enum": ["none", "mild", "moderate", "severe"],
          "description": "Vulvar irritation severity"
        }
      }
    },
    "SystemicSymptoms": {
      "type": "object",
      "required": ["fatigue", "nausea", "fever"],
      "properties": {
        "fatigue": {
          "oneOf": [
            {
              "type": "string",
              "enum": ["none", "mild", "moderate", "severe"]
            },
            {
              "type": "string"
            }
          ],
          "description": "Fatigue level"
        },
        "dizziness": {
          "type": "string",
          "enum": ["none", "mild", "moderate", "severe"],
          "description": "Dizziness severity"
        },
        "nausea": {
          "type": "boolean",
          "description": "Nausea presence"
        },
        "fever": {
          "type": "boolean",
          "description": "Fever presence"
        },
        "weight_change": {
          "type": "string",
          "description": "Weight change"
        }
      }
    },
    "MedicalContext": {
      "type": "object",
      "properties": {
        "current_medications": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Current medications"
        },
        "recent_medications": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Recent medications"
        },
        "medical_conditions": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Medical conditions"
        },
        "previous_gynecological_issues": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Previous gynecological issues"
        },
        "allergies": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Drug allergies - CRITICAL for safety"
        },
        "family_history": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Family medical history"
        }
      }
    },
    "HealthcareInteraction": {
      "type": "object",
      "required": ["previous_consultation", "investigations_done"],
      "properties": {
        "previous_consultation": {
          "type": "boolean",
          "description": "Previous consultation status"
        },
        "consultation_outcome": {
          "type": "string",
          "description": "Previous consultation outcome"
        },
        "investigations_done": {
          "type": "boolean",
          "description": "Investigations done status"
        },
        "investigation_results": {
          "type": "string",
          "description": "Investigation results"
        },
        "current_treatment": {
          "type": "string",
          "description": "Current treatment"
        }
      }
    },
    "PatientConcerns": {
      "type": "object",
      "required": ["main_worry", "impact_on_life"],
      "properties": {
        "main_worry": {
          "type": "string",
          "description": "Patient's main worry"
        },
        "impact_on_life": {
          "type": "string",
          "description": "Impact on patient's life"
        },
        "additional_notes": {
          "type": "string",
          "description": "Additional notes from patient"
        }
      }
    }
  }
}
```

### StructuredDiagnosisResponse Schema

**Endpoint Response:** `POST /api/v1/diagnosis/structured`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "title": "StructuredDiagnosisResponse",
  "description": "Comprehensive response for structured diagnosis",
  "required": [
    "request_id",
    "patient_age", 
    "primary_symptom",
    "possible_diagnoses",
    "clinical_reasoning",
    "safety_assessment",
    "risk_assessment",
    "treatment_recommendations",
    "confidence_score",
    "disclaimer"
  ],
  "properties": {
    "request_id": {
      "type": "string",
      "description": "Original request ID"
    },
    "patient_age": {
      "type": "integer",
      "description": "Patient age"
    },
    "primary_symptom": {
      "type": "string",
      "description": "Primary symptom analyzed"
    },
    "possible_diagnoses": {
      "type": "array",
      "minItems": 1,
      "maxItems": 3,
      "items": { "$ref": "#/$defs/PossibleDiagnosis" },
      "description": "List of possible diagnoses with confidence scores"
    },
    "clinical_reasoning": {
      "type": "string",
      "description": "Clinical reasoning behind the diagnosis"
    },
    "differential_considerations": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Differential diagnosis considerations"
    },
    "safety_assessment": {
      "$ref": "#/$defs/SafetyAssessment"
    },
    "risk_assessment": {
      "$ref": "#/$defs/RiskAssessment"
    },
    "recommended_investigations": {
      "type": "array",
      "items": { "$ref": "#/$defs/Investigation" },
      "description": "Recommended investigations and tests"
    },
    "treatment_recommendations": {
      "$ref": "#/$defs/TreatmentRecommendation"
    },
    "patient_education": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Patient education points"
    },
    "warning_signs": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Warning signs to watch for"
    },
    "confidence_score": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Overall confidence score"
    },
    "processing_notes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Processing notes and considerations"
    },
    "disclaimer": {
      "type": "string",
      "description": "Medical disclaimer"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Response timestamp"
    }
  },
  "$defs": {
    "PossibleDiagnosis": {
      "type": "object",
      "required": ["name", "confidence_score"],
      "properties": {
        "name": {
          "type": "string",
          "description": "Diagnosis name"
        },
        "confidence_score": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0,
          "description": "Confidence score for this diagnosis"
        },
        "description": {
          "type": "string",
          "description": "Brief diagnosis description"
        }
      }
    },
    "SafetyAssessment": {
      "type": "object",
      "required": ["allergy_considerations"],
      "properties": {
        "allergy_considerations": {
          "$ref": "#/$defs/AllergyConsideration"
        },
        "condition_interactions": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Interactions with existing conditions"
        },
        "safety_warnings": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Important safety warnings"
        }
      }
    },
    "AllergyConsideration": {
      "type": "object",
      "properties": {
        "allergic_medications": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Medications patient is allergic to"
        },
        "safe_alternatives": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Safe alternative medications"
        },
        "contraindicated_drugs": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Drugs to avoid"
        }
      }
    },
    "RiskAssessment": {
      "type": "object",
      "required": ["urgency_level"],
      "properties": {
        "urgency_level": {
          "type": "string",
          "enum": ["low", "moderate", "high", "urgent"],
          "description": "Urgency level"
        },
        "red_flags": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Red flag symptoms to watch for"
        },
        "when_to_seek_emergency_care": {
          "type": "array",
          "items": { "type": "string" },
          "description": "When to seek emergency care"
        }
      }
    },
    "TreatmentRecommendation": {
      "type": "object",
      "required": ["follow_up_timeline"],
      "properties": {
        "primary_treatment": {
          "type": "string",
          "description": "Primary recommended treatment"
        },
        "safe_medications": {
          "type": "array",
          "items": { "$ref": "#/$defs/Medication" },
          "description": "Safe medications considering allergies"
        },
        "lifestyle_modifications": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Lifestyle modification recommendations"
        },
        "dietary_advice": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Dietary recommendations"
        },
        "follow_up_timeline": {
          "type": "string",
          "description": "Recommended follow-up timeline"
        }
      }
    }
  }
}
```

---

## 🏥 Health Check Endpoints

### HealthCheckResponse Schema

**Endpoints:** 
- `GET /api/v1/health/`
- `GET /api/v1/health/live`
- `GET /api/v1/health/ready`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "title": "HealthCheckResponse",
  "description": "Health check response for service monitoring",
  "required": ["status", "version"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["healthy", "degraded", "unhealthy", "alive", "ready", "not_ready"],
      "description": "Service status"
    },
    "version": {
      "type": "string",
      "description": "API version"
    },
    "services": {
      "type": "object",
      "description": "External service status",
      "properties": {
        "openai": {
          "type": "string",
          "enum": ["healthy", "unhealthy"],
          "description": "OpenAI service status"
        },
        "redis": {
          "type": "string", 
          "enum": ["healthy", "unhealthy"],
          "description": "Redis service status"
        }
      }
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Health check timestamp"
    },
    "reason": {
      "type": "string",
      "description": "Reason for not_ready status (readiness probe only)"
    }
  }
}
```

---

## ❌ Error Handling

### ErrorResponse Schema

**All endpoints** - returned on errors with appropriate HTTP status codes

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "title": "ErrorResponse",
  "description": "Standard error response format",
  "required": ["error"],
  "properties": {
    "error": {
      "type": "string",
      "description": "Error message"
    },
    "error_code": {
      "type": "string",
      "description": "Machine-readable error code",
      "enum": [
        "OPENAI_SERVICE_ERROR",
        "DIAGNOSIS_SERVICE_ERROR", 
        "AUTHENTICATION_ERROR",
        "RATE_LIMIT_ERROR",
        "VALIDATION_ERROR"
      ]
    },
    "detail": {
      "type": "string",
      "description": "Detailed error explanation"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Error timestamp"
    }
  },
  "example": {
    "error": "Invalid input",
    "error_code": "VALIDATION_ERROR", 
    "detail": "Symptoms list cannot be empty",
    "timestamp": "2023-11-15T10:30:00Z"
  }
}
```

---

## 📊 Key Schema Validation Rules

### ✅ **Critical Validations**

1. **Patient Age**: 12-100 years (reproductive age focus)
2. **Symptoms**: 1-20 items, 2-100 characters each
3. **Drug Allergies**: Cross-validated against medication recommendations
4. **Confidence Score**: 0.0-1.0 range with semantic meaning
5. **Timestamps**: ISO 8601 format required
6. **Request ID**: Minimum 3 characters for tracking

### 🔐 **Security Validations**

1. **Input Sanitization**: All string fields validated and sanitized
2. **Length Limits**: Prevents injection attacks and overflow
3. **Enum Validation**: Restricts values to predefined safe options
4. **Medical Safety**: Allergy checking integrated into schema validation

### 📈 **Performance Considerations**

1. **Array Limits**: Maximum items to prevent excessive processing
2. **String Lengths**: Balanced between usability and performance
3. **Optional Fields**: Many fields optional to reduce payload size
4. **Nested Validation**: Efficient validation of complex nested structures

This JSON Schema documentation provides the complete contract for integrating with the Tenderly AI Agent API, ensuring type safety, validation, and clear expectations for all endpoints.
