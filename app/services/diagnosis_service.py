"""Main diagnosis service for processing input and generating diagnosis."""

from typing import Dict, Any, Optional
from app.models import DiagnosisRequest, DiagnosisResponse, StructuredDiagnosisRequest, StructuredDiagnosisResponse
from app.services.openai_service import openai_service
from app.config.settings import settings
from app.utils.logger import get_logger
from app.exceptions.custom_exceptions import DiagnosisServiceError

logger = get_logger(__name__)


class DiagnosisService:
    """Main service for handling diagnosis logic."""

    @staticmethod
    async def process_diagnosis_request(request: DiagnosisRequest) -> DiagnosisResponse:
        """
        Process diagnosis request and generate response.

        Args:
            request: DiagnosisRequest containing input data

        Returns:
            DiagnosisResponse with predicted diagnosis and recommendations

        Raises:
            DiagnosisServiceError: On processing failure
        """
        try:
            logger.info(f"Processing diagnosis request for patient age {request.patient_age}")

            # Generate diagnosis using OpenAI
            diagnosis_data = await openai_service.generate_diagnosis(
                symptoms=request.symptoms,
                patient_age=request.patient_age,
                medical_history=None,  # Not included in simplified model
                severity_level=request.severity_level.value,
                duration=request.duration,
                onset=request.onset.value if request.onset else None,
                progression=request.progression.value if request.progression else None,
                additional_notes=None,  # Not included in simplified model
            )

            # Compose response
            response = DiagnosisResponse(
                diagnosis=diagnosis_data.get("diagnosis", "Unknown"),
                confidence_score=diagnosis_data.get("confidence_score", 0.0),
                suggested_investigations=diagnosis_data.get("suggested_investigations", []),
                recommended_medications=[{
                    "name": med.get("name", "Unknown"),
                    "dosage": med.get("dosage", ""),
                    "frequency": med.get("frequency", ""),
                    "duration": med.get("duration", ""),
                    "reason": med.get("reason", "Not provided"),
                    "notes": med.get("notes", "")
                } for med in diagnosis_data.get("recommended_medications", [])],
                lifestyle_advice=diagnosis_data.get("lifestyle_advice", []),
                follow_up_recommendations=diagnosis_data.get("follow_up_recommendations", ""),
                disclaimer=settings.medical_disclaimer
            )

            logger.info(f"Successfully processed diagnosis request with confidence score {response.confidence_score}")

            return response

        except Exception as e:
            logger.error(f"Diagnosis processing failed: {e}")
            raise DiagnosisServiceError(f"Diagnosis processing failed: {e}")

    @staticmethod
    async def process_structured_diagnosis_request(request: StructuredDiagnosisRequest) -> StructuredDiagnosisResponse:
        """
        Process structured diagnosis request and generate comprehensive response.

        Args:
            request: StructuredDiagnosisRequest containing detailed input data

        Returns:
            StructuredDiagnosisResponse with detailed diagnosis findings and recommendations

        Raises:
            DiagnosisServiceError: On processing failure
        """
        try:
            logger.info(f"Processing structured diagnosis request for request ID {request.patient_profile.request_id}")

            # Extract patient details and primary complaint
            patient_age = request.patient_profile.age
            primary_symptom = request.primary_complaint.main_symptom

            # Generate a detailed diagnosis using OpenAI or similar service
            diagnosis_data = await openai_service.generate_structured_diagnosis(request=request.dict())

            # Compose the structured response
            response = StructuredDiagnosisResponse(
                request_id=request.patient_profile.request_id,
                patient_age=patient_age,
                primary_symptom=primary_symptom,
                possible_diagnoses=diagnosis_data.get("possible_diagnoses", []),
                clinical_reasoning=diagnosis_data.get("clinical_reasoning", ""),
                differential_considerations=diagnosis_data.get("differential_considerations", []),
                safety_assessment=diagnosis_data.get("safety_assessment"),
                risk_assessment=diagnosis_data.get("risk_assessment"),
                recommended_investigations=diagnosis_data.get("recommended_investigations", []),
                treatment_recommendations=diagnosis_data.get("treatment_recommendations"),
                patient_education=diagnosis_data.get("patient_education", []),
                warning_signs=diagnosis_data.get("warning_signs", []),
                confidence_score=diagnosis_data.get("confidence_score", 0.0),
                processing_notes=diagnosis_data.get("processing_notes", []),
                disclaimer=settings.medical_disclaimer,
            )

            logger.info(f"Successfully processed structured diagnosis request with confidence score {response.confidence_score}")

            return response

        except Exception as e:
            logger.error(f"Structured diagnosis processing failed: {e}")
            raise DiagnosisServiceError(f"Structured diagnosis processing failed: {e}")



# Global diagnosis service instance
diagnosis_service = DiagnosisService()
