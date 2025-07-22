"""Diagnosis router with endpoints for AI diagnosis."""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models import (
    DiagnosisRequest, 
    DiagnosisResponse, 
    ErrorResponse, 
    StructuredDiagnosisRequest,
    StructuredDiagnosisResponse
)
from app.models.simplified_structured_request import SimplifiedStructuredDiagnosisRequest
from app.services.diagnosis_service import diagnosis_service
from app.middleware.auth import get_current_user
from app.middleware.rate_limiter import check_rate_limit_dependency
from app.utils.logger import get_logger
from app.exceptions.custom_exceptions import (
    DiagnosisServiceError,
    OpenAIServiceError,
    RateLimitError
)
from app.services.openai_service import openai_service
from app.config.settings import settings

logger = get_logger(__name__)

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])


@router.post(
    "/",
    response_model=DiagnosisResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate AI diagnosis",
    description="Generate AI diagnosis based on symptoms and patient information",
    responses={
        200: {
            "description": "Successful diagnosis generation",
            "model": DiagnosisResponse,
        },
        400: {
            "description": "Invalid request",
            "model": ErrorResponse,
        },
        401: {
            "description": "Unauthorized",
            "model": ErrorResponse,
        },
        429: {
            "description": "Rate limit exceeded",
            "model": ErrorResponse,
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse,
        },
    },
)
async def generate_diagnosis(
    diagnosis_request: DiagnosisRequest,
    current_user: dict = Depends(get_current_user),
    _: None = Depends(check_rate_limit_dependency),
) -> DiagnosisResponse:
    """
    Generate AI diagnosis based on symptoms and patient information.
    
    Args:
        request: FastAPI request object
        diagnosis_request: Patient symptoms and information
        current_user: Current authenticated user
        
    Returns:
        AI-generated diagnosis with recommendations
        
    Raises:
        HTTPException: On processing errors
    """
    try:
        logger.info(
            f"Processing diagnosis request",
            extra={
                "user_id": current_user.get("sub"),
                "symptoms_count": len(diagnosis_request.symptoms),
                "patient_age": diagnosis_request.patient_age,
                "severity": diagnosis_request.severity_level.value,
            }
        )
        
        # Process diagnosis request
        diagnosis_response = await diagnosis_service.process_diagnosis_request(
            diagnosis_request
        )
        
        logger.info(
            f"Diagnosis generated successfully",
            extra={
                "user_id": current_user.get("sub"),
                "diagnosis": diagnosis_response.diagnosis,
                "confidence_score": diagnosis_response.confidence_score,
            }
        )
        
        return diagnosis_response
        
    except DiagnosisServiceError as e:
        logger.error(f"Diagnosis service error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Diagnosis processing failed: {str(e)}",
        )
    except OpenAIServiceError as e:
        logger.error(f"OpenAI service error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service temporarily unavailable: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Unexpected error in diagnosis endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing diagnosis",
        )


@router.post(
    "/validate",
    status_code=status.HTTP_200_OK,
    summary="Validate symptoms",
    description="Validate symptoms input without generating diagnosis",
    responses={
        200: {
            "description": "Symptoms validation result",
        },
        400: {
            "description": "Invalid request",
            "model": ErrorResponse,
        },
        401: {
            "description": "Unauthorized",
            "model": ErrorResponse,
        },
    },
)
async def validate_symptoms(
    symptoms: list[str],
    current_user: dict = Depends(get_current_user),
) -> dict:
    """
    Validate symptoms input without generating diagnosis.
    
    Args:
        symptoms: List of symptoms to validate
        current_user: Current authenticated user
        
    Returns:
        Validation result
    """
    try:
        logger.info(
            f"Validating symptoms",
            extra={
                "user_id": current_user.get("sub"),
                "symptoms_count": len(symptoms),
            }
        )
        
        # Simple validation - check if symptoms are not empty and reasonable
        valid_symptoms = []
        invalid_symptoms = []
        
        for symptom in symptoms:
            if isinstance(symptom, str) and 2 <= len(symptom.strip()) <= 100:
                valid_symptoms.append(symptom.strip().lower())
            else:
                invalid_symptoms.append(symptom)
        
        return {
            "valid_symptoms": valid_symptoms,
            "invalid_symptoms": invalid_symptoms,
            "total_symptoms": len(symptoms),
            "valid_count": len(valid_symptoms),
            "invalid_count": len(invalid_symptoms),
        }
        
    except Exception as e:
        logger.error(f"Symptoms validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while validating symptoms",
        )






@router.post(
    "/structure",
    response_model=StructuredDiagnosisResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate simplified structured AI diagnosis",
    description="Generate AI diagnosis using simplified structured patient data",
    responses={
        200: {
            "description": "Successful diagnosis generation",
            "model": StructuredDiagnosisResponse,
        },
        400: {
            "description": "Invalid request data",
            "model": ErrorResponse,
        },
        401: {
            "description": "Unauthorized",
            "model": ErrorResponse,
        },
        429: {
            "description": "Rate limit exceeded",
            "model": ErrorResponse,
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse,
        },
        503: {
            "description": "AI service temporarily unavailable",
            "model": ErrorResponse,
        },
    },
)
async def generate_simplified_structured_diagnosis(
    structured_request: SimplifiedStructuredDiagnosisRequest,
    current_user: dict = Depends(get_current_user),
    _: None = Depends(check_rate_limit_dependency),
) -> StructuredDiagnosisResponse:
    """
    Generate AI diagnosis using simplified structured patient data.
    
    This endpoint accepts simplified structured patient data and generates
    comprehensive diagnosis with safety considerations.
    
    Args:
        structured_request: Simplified structured patient data
        current_user: Current authenticated user
        
    Returns:
        Comprehensive structured diagnosis with safety considerations
        
    Raises:
        HTTPException: On validation errors, service failures, or processing errors
    """
    try:
        logger.info(
            f"Processing simplified structured diagnosis request",
            extra={
                "user_id": current_user.get("sub"),
                "request_id": structured_request.patient_profile.request_id,
                "patient_age": structured_request.patient_profile.age,
                "primary_symptom": structured_request.primary_complaint.main_symptom,
                "severity": structured_request.primary_complaint.severity,
                "allergies_count": len(structured_request.medical_context.allergies),
            }
        )
        
        # Convert to dict for OpenAI processing
        request_dict = structured_request.dict()
        
        # Generate diagnosis using OpenAI
        diagnosis_data = await openai_service.generate_structured_diagnosis(request=request_dict)
        
        # Compose the structured response
        from app.models.structured_response import (
            StructuredDiagnosisResponse,
            SafetyAssessment, 
            AllergyConsideration,
            RiskAssessment,
            TreatmentRecommendation
        )
        from app.models.response import PossibleDiagnosis
        
        response = StructuredDiagnosisResponse(
            request_id=structured_request.patient_profile.request_id,
            patient_age=structured_request.patient_profile.age,
            primary_symptom=structured_request.primary_complaint.main_symptom,
            possible_diagnoses=[PossibleDiagnosis(**diag) for diag in diagnosis_data.get("possible_diagnoses", [])],
            clinical_reasoning=diagnosis_data.get("clinical_reasoning", ""),
            differential_considerations=diagnosis_data.get("differential_considerations", []),
            safety_assessment=SafetyAssessment(
                allergy_considerations=AllergyConsideration(**diagnosis_data.get("safety_assessment", {}).get("allergy_considerations", {})),
                condition_interactions=diagnosis_data.get("safety_assessment", {}).get("condition_interactions", []),
                safety_warnings=diagnosis_data.get("safety_assessment", {}).get("safety_warnings", [])
            ),
            risk_assessment=RiskAssessment(**diagnosis_data.get("risk_assessment", {})),
            recommended_investigations=diagnosis_data.get("recommended_investigations", []),
            treatment_recommendations=TreatmentRecommendation(**diagnosis_data.get("treatment_recommendations", {})),
            patient_education=diagnosis_data.get("patient_education", []),
            warning_signs=diagnosis_data.get("warning_signs", []),
            confidence_score=diagnosis_data.get("confidence_score", 0.0),
            processing_notes=diagnosis_data.get("processing_notes", []),
            disclaimer=settings.medical_disclaimer,
        )
        
        logger.info(
            f"Simplified structured diagnosis generated successfully",
            extra={
                "user_id": current_user.get("sub"),
                "request_id": structured_request.patient_profile.request_id,
                "primary_diagnosis": response.possible_diagnoses[0].name if response.possible_diagnoses else "Unknown",
                "confidence_score": response.confidence_score,
            }
        )
        
        return response
        
    except Exception as e:
        logger.error(
            f"Simplified structured diagnosis error: {e}",
            extra={
                "user_id": current_user.get("sub"),
                "request_id": structured_request.patient_profile.request_id,
                "error": str(e),
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simplified structured diagnosis failed: {str(e)}",
        )


