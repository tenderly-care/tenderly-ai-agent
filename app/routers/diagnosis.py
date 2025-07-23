"""Diagnosis router with endpoints for AI diagnosis."""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models import (
    DiagnosisRequest, 
    DiagnosisResponse, 
    ErrorResponse, 
    StructuredDiagnosisRequest,
    StructuredDiagnosisResponse,
    PossibleDiagnosis,
    Investigation
)
from app.models.response import Medication
from app.models.simplified_structured_request import SimplifiedStructuredDiagnosisRequest
from app.models.structured_response import (
    SafetyAssessment, 
    AllergyConsideration,
    RiskAssessment,
    TreatmentRecommendation
)
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
from app.services.pdf_service import pdf_service
from app.config.settings import settings
from fastapi.responses import StreamingResponse
from datetime import datetime
import io

logger = get_logger(__name__)

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])


async def get_diagnosis_by_request_id(request_id: str) -> StructuredDiagnosisResponse:
    """
    Mock function to simulate retrieval of comprehensive diagnosis data by request ID.
    In a real application, this would query your database.
    
    This function returns complete diagnosis data with all fields populated
    to ensure the PDF contains comprehensive information.
    """
    # This mock implementation should be replaced with real database lookup
    return StructuredDiagnosisResponse(
        request_id=request_id,
        patient_age=28,
        primary_symptom="vaginal_discharge_with_itching",
        possible_diagnoses=[
            PossibleDiagnosis(
                name="Vaginal Candidiasis (Yeast Infection)",
                confidence_score=0.88,
                description="Fungal infection of the vagina caused by Candida albicans, characterized by thick white discharge and intense itching."
            ),
            PossibleDiagnosis(
                name="Bacterial Vaginosis",
                confidence_score=0.65,
                description="Bacterial imbalance in the vaginal flora, typically causing fishy-smelling discharge."
            ),
            PossibleDiagnosis(
                name="Mixed Vaginal Infection",
                confidence_score=0.45,
                description="Combination of bacterial and fungal overgrowth requiring targeted treatment."
            )
        ],
        clinical_reasoning=(
            "Based on the patient's presentation of thick, white, cottage cheese-like vaginal discharge "
            "accompanied by severe itching and burning sensation, along with the absence of fishy odor, "
            "the clinical picture strongly suggests vaginal candidiasis. The patient's recent antibiotic "
            "use and reported stress levels further support this diagnosis, as these are known risk factors "
            "for Candida overgrowth. The normal vaginal pH and positive KOH prep would confirm this diagnosis."
        ),
        differential_considerations=[
            "Bacterial Vaginosis - ruled out due to absence of fishy odor",
            "Trichomoniasis - less likely due to absence of frothy discharge",
            "Vulvovaginal Dermatitis - possible concurrent condition",
            "Sexually Transmitted Infections - screening recommended"
        ],
        safety_assessment=SafetyAssessment(
            allergy_considerations=AllergyConsideration(
                allergic_medications=["fluconazole", "azole antifungals"],
                safe_alternatives=["nystatin", "boric acid suppositories", "topical clotrimazole"],
                contraindicated_drugs=["fluconazole (due to reported allergy)", "other azole medications"]
            ),
            condition_interactions=[
                "Type 2 Diabetes - increases risk of recurrent infections",
                "Recent antibiotic use - contributes to vaginal flora disruption",
                "Hormonal contraceptives - may affect vaginal environment"
            ],
            safety_warnings=[
                "Avoid fluconazole due to documented allergy",
                "Monitor blood glucose levels closely during treatment",
                "Discontinue if severe allergic reaction occurs",
                "Seek immediate care if symptoms worsen or fever develops"
            ]
        ),
        risk_assessment=RiskAssessment(
            urgency_level="moderate",
            red_flags=[
                "Fever above 101°F (38.3°C)",
                "Severe pelvic pain",
                "Heavy bleeding",
                "Signs of systemic infection"
            ],
            when_to_seek_emergency_care=[
                "High fever with severe pelvic pain",
                "Signs of sepsis (confusion, rapid heartbeat, difficulty breathing)",
                "Severe allergic reaction to medications",
                "Inability to urinate due to swelling"
            ]
        ),
        recommended_investigations=[
            Investigation(
                name="Vaginal Wet Mount Microscopy",
                priority="high",
                reason="To visualize yeast cells and hyphae, confirm Candida presence"
            ),
            Investigation(
                name="Vaginal pH Testing",
                priority="high",
                reason="Normal pH (3.8-4.5) supports yeast infection diagnosis"
            ),
            Investigation(
                name="KOH Preparation Test",
                priority="high",
                reason="KOH prep will dissolve bacteria and reveal fungal elements"
            ),
            Investigation(
                name="Comprehensive STI Screening",
                priority="medium",
                reason="Rule out concurrent sexually transmitted infections"
            ),
            Investigation(
                name="HbA1c (Diabetic Control)",
                priority="medium",
                reason="Assess diabetes control as contributing factor"
            )
        ],
        treatment_recommendations=TreatmentRecommendation(
            primary_treatment=(
                "Topical Nystatin 100,000 units vaginal tablet, insert one tablet daily at bedtime for 14 days. "
                "Alternative: Clotrimazole 1% cream, apply intravaginally once daily for 7 days."
            ),
            safe_medications=[
                Medication(name="Nystatin", dosage="100,000 units vaginal tablet", frequency="Once daily", duration="14 days", reason="Treat vaginal candidiasis", notes="Inserted at bedtime"),
                Medication(name="Clotrimazole", dosage="1% vaginal cream", frequency="Once daily", duration="7 days", reason="Alternative antifungal treatment", notes="Apply intravaginally"),
                Medication(name="Boric acid suppositories", dosage="600mg", frequency="As needed", duration="2 weeks maintenance", reason="Prevent recurrence", notes="As maintenance therapy"),
                Medication(name="Probiotics", dosage="Capsule", frequency="Daily", duration="Ongoing", reason="Support healthy vaginal flora", notes="Contains Lactobacillus strains")
            ],
            lifestyle_modifications=[
                "Wear loose-fitting, breathable cotton underwear",
                "Avoid douching and scented feminine products",
                "Change out of wet clothing promptly (swimsuits, workout clothes)",
                "Sleep without underwear when possible to improve air circulation",
                "Avoid tight-fitting synthetic clothing",
                "Practice good menstrual hygiene"
            ],
            dietary_advice=[
                "Reduce refined sugar and processed carbohydrate intake",
                "Increase consumption of probiotic-rich foods (yogurt, kefir, sauerkraut)",
                "Consider a low-glycemic diet to help control blood sugar",
                "Stay well-hydrated with water",
                "Limit alcohol consumption",
                "Add antifungal foods like garlic, coconut oil, and oregano"
            ],
            follow_up_timeline=(
                "Return in 1 week if symptoms persist or worsen. Schedule routine follow-up in 4 weeks "
                "to ensure complete resolution. For diabetic patients, coordinate with endocrinologist "
                "for optimal glucose control."
            )
        ),
        patient_education=[
            "Complete the full course of treatment even if symptoms improve early",
            "Yeast infections are not sexually transmitted but can be triggered by various factors",
            "Maintain good blood sugar control to prevent recurrent infections",
            "Recognize early symptoms for prompt treatment of future episodes",
            "Understand that some discharge is normal - learn to identify abnormal changes",
            "Know when to seek immediate medical attention (fever, severe pain)",
            "Consider probiotic supplements to maintain healthy vaginal flora"
        ],
        warning_signs=[
            "Worsening symptoms after 3 days of treatment",
            "Development of fever or chills",
            "Severe abdominal or pelvic pain",
            "Heavy or unusual bleeding",
            "Signs of allergic reaction (rash, difficulty breathing, swelling)",
            "Recurrent infections (more than 4 per year)",
            "Symptoms that completely resolve but return within 2 weeks"
        ],
        confidence_score=0.88,
        processing_notes=[
            "Patient history of diabetes increases recurrence risk",
            "Recent antibiotic use likely contributed to current infection",
            "Allergy to fluconazole limits first-line treatment options",
            "Consider maintenance therapy if recurrent episodes occur",
            "Coordinate care with primary care physician for diabetes management"
        ],
        disclaimer=settings.medical_disclaimer,
    )


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


@router.get(
    "/structure/{request_id}/pdf",
    summary="Generate PDF report for structured diagnosis",
    description="Generate a professional PDF report of the structured diagnosis",
    responses={
        200: {
            "description": "PDF report generated successfully",
            "content": {
                "application/pdf": {
                    "schema": {
                        "type": "string",
                        "format": "binary"
                    }
                }
            }
        },
        404: {
            "description": "Diagnosis not found",
            "model": ErrorResponse,
        },
        401: {
            "description": "Unauthorized",
            "model": ErrorResponse,
        },
        500: {
            "description": "PDF generation failed",
            "model": ErrorResponse,
        },
    },
)
async def generate_diagnosis_pdf(
    request_id: str,
    current_user: dict = Depends(get_current_user),
    doctor_notes: str = None,
    clinic_name: str = None,
    clinic_address: str = None,
) -> StreamingResponse:
    """
    Generate a professional PDF report for structured diagnosis.
    
    Args:
        request_id: The diagnosis request ID
        current_user: Current authenticated user
        doctor_notes: Optional additional notes from the reviewing doctor
        clinic_name: Optional clinic/hospital name for header
        clinic_address: Optional clinic/hospital address for header
        
    Returns:
        StreamingResponse: PDF file as streaming response
        
    Raises:
        HTTPException: On PDF generation errors or diagnosis not found
    """
    try:
        logger.info(
            f"Generating PDF for request ID: {request_id}",
            extra={
                "user_id": current_user.get("sub"),
                "request_id": request_id,
            }
        )
        
        # Retrieve diagnosis data using the mock function
        diagnosis_data = await get_diagnosis_by_request_id(request_id)
        
        # Prepare clinic info if provided
        clinic_info = None
        if clinic_name:
            clinic_info = {
                "name": clinic_name,
                "address": clinic_address
            }
        
        # Generate PDF using the retrieved diagnosis data
        pdf_buffer = await pdf_service.generate_diagnosis_pdf(
            diagnosis_data=diagnosis_data,
            doctor_notes=doctor_notes,
            clinic_info=clinic_info
        )
        
        # Prepare response headers
        filename = f"diagnosis_report_{request_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        headers = {
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "application/pdf"
        }
        
        logger.info(
            f"PDF generated successfully for request ID: {request_id}",
            extra={
                "user_id": current_user.get("sub"),
                "request_id": request_id,
                "filename": filename,
            }
        )
        
        return StreamingResponse(
            io.BytesIO(pdf_buffer.read()),
            media_type="application/pdf",
            headers=headers
        )
        
    except FileNotFoundError:
        logger.error(f"Diagnosis not found for request ID: {request_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Diagnosis not found for request ID: {request_id}",
        )
    except Exception as e:
        logger.error(
            f"PDF generation failed for request ID: {request_id}: {e}",
            extra={
                "user_id": current_user.get("sub"),
                "request_id": request_id,
                "error": str(e),
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF generation failed: {str(e)}",
        )

