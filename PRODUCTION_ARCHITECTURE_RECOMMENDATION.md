# Production Architecture Recommendation

## Overview
Keep the dynamic symptom questioning logic in your main backend, use tenderly-ai-agent as a pure AI processing microservice.

## Backend Components (Your Main API)

### 1. Symptom Configuration System

```python
# models/symptom_config.py
class SymptomConfig:
    symptom_type: str
    questions: List[SymptomQuestion]
    required_fields: List[str]
    validation_rules: Dict[str, Any]

class SymptomQuestion:
    question_id: str
    question_text: str
    input_type: str  # "text", "select", "multi_select", "range"
    options: Optional[List[str]]
    required: bool
    conditional_logic: Optional[Dict]
```

### 2. Dynamic Question Service

```python
# services/symptom_service.py
class SymptomQuestionService:
    
    async def get_questions_for_symptom(self, primary_symptom: str) -> List[SymptomQuestion]:
        """Get dynamic questions based on primary symptom"""
        config = await self.symptom_config_repo.get_by_symptom(primary_symptom)
        return self._apply_conditional_logic(config.questions)
    
    async def validate_responses(self, symptom_type: str, responses: Dict) -> ValidationResult:
        """Validate user responses against symptom config"""
        config = await self.symptom_config_repo.get_by_symptom(symptom_type)
        return self._validate_against_rules(config.validation_rules, responses)
    
    async def build_structured_request(self, patient_data: Dict, responses: Dict) -> NewStructuredDiagnosisRequest:
        """Build the structured request for AI agent"""
        return NewStructuredDiagnosisRequest(
            patient_profile=patient_data,
            primary_complaint=self._extract_primary_complaint(responses),
            symptom_specific_details=responses,
            # ... other fields
        )
```

### 3. Your Backend API Endpoints

```python
# routers/diagnosis.py in your main backend

@router.get("/symptoms/{symptom_type}/questions")
async def get_dynamic_questions(symptom_type: str):
    """Get questions specific to the selected symptom"""
    questions = await symptom_service.get_questions_for_symptom(symptom_type)
    return {"questions": questions}

@router.post("/symptoms/validate")
async def validate_symptom_responses(request: SymptomResponseRequest):
    """Validate user responses before sending to AI"""
    validation = await symptom_service.validate_responses(
        request.symptom_type, 
        request.responses
    )
    return {"valid": validation.is_valid, "errors": validation.errors}

@router.post("/diagnosis/generate")
async def generate_diagnosis(request: DiagnosisRequestData):
    """Main endpoint that orchestrates the diagnosis flow"""
    
    # 1. Build structured request
    structured_request = await symptom_service.build_structured_request(
        request.patient_data, 
        request.symptom_responses
    )
    
    # 2. Call AI agent
    ai_response = await tenderly_ai_client.generate_structured_diagnosis(structured_request)
    
    # 3. Save to database, audit, etc.
    diagnosis_record = await diagnosis_repo.save(ai_response, request.patient_id)
    
    # 4. Return enhanced response
    return {
        "diagnosis": ai_response,
        "record_id": diagnosis_record.id,
        "follow_up_scheduled": await self._schedule_follow_up(ai_response)
    }
```

## AI Agent Responsibilities (tenderly-ai-agent)

Keep your current `tenderly-ai-agent` focused on:

- ✅ Receiving fully structured requests
- ✅ AI processing and prompt engineering
- ✅ OpenAI API integration
- ✅ Response formatting
- ✅ Error handling for AI-specific issues

## Data Flow

1. **Frontend** → Select primary symptom
2. **Backend** → Return dynamic questions for that symptom
3. **Frontend** → User fills out symptom-specific questions
4. **Backend** → Validate responses, build structured request
5. **Backend** → Send structured request to AI agent
6. **AI Agent** → Process with OpenAI, return diagnosis
7. **Backend** → Save, audit, enhance response
8. **Frontend** → Display diagnosis with follow-up options

## Configuration Management

```python
# Example symptom configurations
SYMPTOM_CONFIGS = {
    "irregular_bleeding": {
        "questions": [
            {
                "id": "bleeding_pattern",
                "text": "How would you describe your bleeding pattern?",
                "type": "select",
                "options": ["Heavy", "Light", "Spotting", "Intermittent"],
                "required": True
            },
            {
                "id": "cycle_length",
                "text": "What is your typical cycle length?",
                "type": "range",
                "min": 21, "max": 35,
                "required": True
            }
        ]
    },
    "pelvic_pain": {
        "questions": [
            {
                "id": "pain_location",
                "text": "Where is the pain located?",
                "type": "multi_select", 
                "options": ["Lower abdomen", "Pelvis", "Lower back", "Vaginal area"],
                "required": True
            }
        ]
    }
}
```

## Benefits of This Approach

### Business Logic Control
- Complete control over symptom questioning flow
- Easy to modify questions without touching AI service
- A/B testing of question sets
- Integration with patient history and preferences

### Data Management  
- All patient interactions logged in your database
- Easy analytics on symptom patterns and outcomes
- HIPAA compliance and audit trails
- Integration with EHR systems

### Flexibility
- Support multiple AI providers (not just OpenAI)
- Gradual rollout of new symptom types
- Different question sets for different user segments
- Integration with telehealth workflows

### Performance
- Cache symptom configurations
- Batch process multiple questions
- Offline capability for questions
- Reduced AI agent calls (only when ready for diagnosis)

## Implementation Priority

1. **Phase 1**: Implement symptom configuration system in your backend
2. **Phase 2**: Create dynamic question API endpoints  
3. **Phase 3**: Update frontend to use dynamic questions
4. **Phase 4**: Keep existing AI agent endpoints, add new structured endpoint
5. **Phase 5**: Implement enhanced backend orchestration

This approach gives you maximum flexibility while keeping your AI agent focused and efficient.
