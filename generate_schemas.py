#!/usr/bin/env python3
"""Generate JSON schemas for all Tenderly AI Agent models."""

import sys
import os
sys.path.insert(0, '.')

from app.models.request import DiagnosisRequest, SymptomValidationRequest
from app.models.response import DiagnosisResponse, HealthCheckResponse, ErrorResponse, Medication, Investigation
from app.models.structured_request import StructuredDiagnosisRequest
from app.models.structured_response import StructuredDiagnosisResponse
from app.models.new_structured_request import NewStructuredDiagnosisRequest
from app.models.new_structured_response import NewStructuredDiagnosisResponse
from app.models.wrappers import StructuredDiagnosisRequestWrapper
import json

def generate_schema_file():
    schemas = {
        "simple_diagnosis_request": DiagnosisRequest.model_json_schema(),
        "simple_diagnosis_response": DiagnosisResponse.model_json_schema(),
        "structured_diagnosis_request": StructuredDiagnosisRequest.model_json_schema(),
        "structured_diagnosis_response": StructuredDiagnosisResponse.model_json_schema(),
        "new_structured_diagnosis_request": NewStructuredDiagnosisRequest.model_json_schema(),
        "new_structured_diagnosis_response": NewStructuredDiagnosisResponse.model_json_schema(),
        "health_check_response": HealthCheckResponse.model_json_schema(),
        "error_response": ErrorResponse.model_json_schema(),
        "medication": Medication.model_json_schema(),
        "investigation": Investigation.model_json_schema(),
        "symptom_validation_request": SymptomValidationRequest.model_json_schema(),
        "structured_request_wrapper": StructuredDiagnosisRequestWrapper.model_json_schema()
    }
    
    return schemas

if __name__ == "__main__":
    schemas = generate_schema_file()
    
    # Print all schemas
    for schema_name, schema_data in schemas.items():
        print(f"\n{'='*80}")
        print(f"=== {schema_name.upper()} SCHEMA ===")
        print('='*80)
        print(json.dumps(schema_data, indent=2))
        print()
