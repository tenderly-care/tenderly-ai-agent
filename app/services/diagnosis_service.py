"""Main diagnosis service for processing input and generating diagnosis."""

from typing import Dict, Any, Optional
from app.models import DiagnosisRequest, DiagnosisResponse
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


# Global diagnosis service instance
diagnosis_service = DiagnosisService()
