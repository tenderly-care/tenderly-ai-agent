# 🧪 Structured Diagnosis Testing Guide

This guide provides comprehensive instructions for testing the structured diagnosis endpoints of your Tenderly AI Agent.

## 🎯 Available Endpoints

### 1. Test Endpoint (No Authentication)
- **URL**: `POST /api/v1/diagnosis/structured/test`
- **Authentication**: Not required
- **Purpose**: Testing and development

### 2. Production Endpoint (Authentication Required)
- **URL**: `POST /api/v1/diagnosis/structured`
- **Authentication**: Bearer Token required
- **Purpose**: Production use with user authentication

## 🚀 Quick Testing Commands

### Option 1: Use the Python Test Script (Recommended)
```bash
python test_structured_diagnosis.py
```

### Option 2: Manual curl Commands

#### Test Endpoint (No Auth Required)
```bash
curl -X POST http://localhost:8000/api/v1/diagnosis/structured/test \
  -H "Content-Type: application/json" \
  -d '{
    "patient_profile": {
      "age": 29,
      "request_id": "test_001",
      "timestamp": "2025-07-21T06:30:00Z"
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
        "could_be_pregnant": false
      },
      "sexual_activity": {
        "sexually_active": true,
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
        "nausea": false,
        "fever": false
      }
    },
    "medical_context": {
      "current_medications": [],
      "recent_medications": [],
      "medical_conditions": ["diabetes"],
      "previous_gynecological_issues": ["yeast infections"],
      "allergies": ["penicillin", "amoxicillin"],
      "family_history": []
    },
    "healthcare_interaction": {
      "previous_consultation": true,
      "consultation_outcome": "inconclusive",
      "investigations_done": false,
      "current_treatment": "none"
    },
    "patient_concerns": {
      "main_worry": "recurrent infections",
      "impact_on_life": "moderate",
      "additional_notes": "I have drug allergies"
    }
  }' | jq .
```

#### Authenticated Endpoint
1. First generate a token:
```bash
python generate_token.py
```

2. Then use the token in your request:
```bash
curl -X POST http://localhost:8000/api/v1/diagnosis/structured \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{ ... same JSON as above ... }'
```

## 📋 Test Scenarios

### 1. Vaginal Discharge with Drug Allergies
- **Symptom**: White cottage cheese-like discharge with severe itching
- **Medical History**: Diabetes, previous yeast infections
- **Allergies**: Penicillin, Amoxicillin, Fluconazole
- **Expected**: Safe medication alternatives, allergy considerations

### 2. Severe Pelvic Pain
- **Symptom**: Sudden severe pelvic pain with abnormal bleeding
- **Risk Factors**: Sexually active, no contraception
- **Expected**: High urgency, emergency care guidance

### 3. Missed Period
- **Symptom**: 2 weeks late period with nausea
- **Context**: Taking birth control but missed some pills
- **Expected**: Pregnancy considerations, investigation recommendations

## 🔍 Expected Response Structure

```json
{
  "request_id": "test_001",
  "patient_age": 29,
  "primary_symptom": "vaginal_discharge",
  "possible_diagnoses": [
    {
      "name": "Vulvovaginal Candidiasis (Yeast Infection)",
      "confidence_score": 0.85,
      "description": "Detailed description..."
    }
  ],
  "clinical_reasoning": "Detailed reasoning...",
  "differential_considerations": ["Alternative diagnoses..."],
  "safety_assessment": {
    "allergy_considerations": {
      "allergic_medications": ["penicillin", "amoxicillin"],
      "safe_alternatives": ["fluconazole", "clotrimazole"],
      "contraindicated_drugs": []
    },
    "condition_interactions": ["Diabetes considerations..."],
    "safety_warnings": ["Safety warnings..."]
  },
  "risk_assessment": {
    "urgency_level": "low",
    "red_flags": [],
    "when_to_seek_emergency_care": []
  },
  "recommended_investigations": [
    {
      "name": "Vaginal swab for microscopy and culture",
      "priority": "medium",
      "reason": "To confirm diagnosis"
    }
  ],
  "treatment_recommendations": {
    "primary_treatment": "Antifungal therapy",
    "safe_medications": [
      {
        "name": "Fluconazole (Diflucan)",
        "dosage": "150 mg",
        "frequency": "One-time dose",
        "duration": "Single dose",
        "reason": "Effective treatment",
        "notes": "Safe alternative"
      }
    ],
    "lifestyle_modifications": ["Avoid tight clothing..."],
    "dietary_advice": ["Maintain balanced diet..."],
    "follow_up_timeline": "1-2 weeks"
  },
  "patient_education": ["Educational points..."],
  "warning_signs": ["When to seek help..."],
  "confidence_score": 0.85,
  "processing_notes": ["Additional considerations..."],
  "disclaimer": "Medical disclaimer...",
  "timestamp": "2025-07-21T06:30:00Z"
}
```

## 📊 Key Features Tested

### ✅ What the Structured Diagnosis Provides:

1. **Comprehensive Assessment**:
   - Multiple possible diagnoses with confidence scores
   - Clinical reasoning and differential considerations
   - Risk assessment with urgency levels

2. **Safety Features**:
   - Drug allergy considerations
   - Safe medication alternatives
   - Contraindicated medications
   - Medical condition interactions

3. **Clinical Guidance**:
   - Recommended investigations with priorities
   - Treatment recommendations with safe alternatives
   - Lifestyle and dietary advice
   - Follow-up timelines

4. **Patient Education**:
   - Educational content
   - Warning signs to monitor
   - When to seek emergency care

## 🛠️ Validation Tests

The structured endpoint validates:
- **Patient age**: Must be 12-100 years
- **Timestamp format**: Must be valid ISO format
- **Request ID**: Must be at least 3 characters
- **Symptom-specific details**: Required based on main symptom
- **Drug allergy conflicts**: Checks for medication-allergy conflicts

## 🔧 Troubleshooting

### Common Issues:

1. **422 Validation Error**:
   - Check required fields are present
   - Verify timestamp is in ISO format
   - Ensure symptom-specific details match main symptom

2. **401 Authentication Error**:
   - Generate a fresh token using `python generate_token.py`
   - Ensure token is included in Authorization header

3. **500 Internal Server Error**:
   - Check server logs for detailed error information
   - Verify all required model fields are properly structured

## 📝 Usage Notes

- The test endpoint (`/structured/test`) is perfect for development and testing
- The production endpoint (`/structured`) requires authentication for security
- All responses include comprehensive safety assessments
- Drug allergies are carefully considered in treatment recommendations
- Urgency levels help prioritize patient care

## 🎯 Integration Tips

When integrating with your NestJS backend:
1. Use the authenticated endpoint for production
2. Implement proper error handling for validation failures
3. Store and display safety warnings prominently
4. Consider urgency levels for patient triage
5. Present medication alternatives clearly when allergies are present
