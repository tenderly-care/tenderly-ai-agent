"""OpenAI service for AI diagnosis generation."""

import json
import asyncio
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from app.config import settings
from app.utils.logger import get_logger
from app.exceptions.custom_exceptions import OpenAIServiceError

logger = get_logger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API."""

    def __init__(self):
        """Initialize OpenAI service."""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.max_tokens = settings.openai_max_tokens
        self.temperature = settings.openai_temperature

    async def generate_diagnosis(
        self,
        symptoms: list,
        patient_age: int,
        medical_history: Optional[list] = None,
        severity_level: str = "moderate",
        duration: str = "",
        additional_notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate AI diagnosis based on symptoms and patient information.
        
        Args:
            symptoms: List of symptoms
            patient_age: Patient's age
            medical_history: Optional medical history
            severity_level: Severity of symptoms
            duration: Duration of symptoms
            additional_notes: Additional notes
            
        Returns:
            Dict containing diagnosis information
            
        Raises:
            OpenAIServiceError: If OpenAI API call fails
        """
        try:
            prompt = self._create_diagnosis_prompt(
                symptoms=symptoms,
                patient_age=patient_age,
                medical_history=medical_history,
                severity_level=severity_level,
                duration=duration,
                additional_notes=additional_notes,
            )

            logger.info(f"Generating diagnosis for patient age {patient_age} with {len(symptoms)} symptoms")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                response_format={"type": "json_object"},
            )

            if not response.choices:
                raise OpenAIServiceError("No response from OpenAI API")

            content = response.choices[0].message.content
            if not content:
                raise OpenAIServiceError("Empty response from OpenAI API")

            # Parse JSON response
            diagnosis_data = json.loads(content)
            
            logger.info(f"Successfully generated diagnosis: {diagnosis_data.get('diagnosis', 'Unknown')}")
            
            return diagnosis_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response as JSON: {e}")
            raise OpenAIServiceError(f"Invalid JSON response from OpenAI: {e}")
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise OpenAIServiceError(f"OpenAI API call failed: {e}")

    def _create_diagnosis_prompt(
        self,
        symptoms: list,
        patient_age: int,
        medical_history: Optional[list] = None,
        severity_level: str = "moderate",
        duration: str = "",
        additional_notes: Optional[str] = None,
    ) -> str:
        """Create diagnosis prompt for OpenAI."""
        prompt_parts = [
            f"Patient Information:",
            f"- Age: {patient_age} years",
            f"- Symptoms: {', '.join(symptoms)}",
            f"- Severity: {severity_level}",
            f"- Duration: {duration}",
        ]

        if medical_history:
            prompt_parts.append(f"- Medical History: {', '.join(medical_history)}")

        if additional_notes:
            prompt_parts.append(f"- Additional Notes: {additional_notes}")

        prompt_parts.extend([
            "",
            "Please provide a gynecological diagnosis based on the above information.",
            "Focus on common gynecological conditions that match the symptoms.",
            "Provide specific, actionable recommendations for treatment and follow-up.",
        ])

        return "\n".join(prompt_parts)

    def _get_system_prompt(self) -> str:
        """Get system prompt for OpenAI."""
        return '''You are a specialized AI assistant for gynecological diagnosis. 
        
        Your task is to analyze patient symptoms and provide a structured diagnosis response.
        
        IMPORTANT GUIDELINES:
        1. Focus only on gynecological conditions
        2. Provide evidence-based recommendations
        3. Always include appropriate disclaimers
        4. Suggest follow-up with healthcare providers
        5. Be conservative with medication recommendations
        6. Consider patient age and medical history
        
        RESPONSE FORMAT:
        You must respond with a valid JSON object containing:
        {
            "diagnosis": "Primary diagnosis name",
            "confidence_score": 0.85,
            "suggested_investigations": [
                {
                    "name": "Investigation name",
                    "priority": "low/medium/high",
                    "reason": "Reason for investigation"
                }
            ],
            "recommended_medications": [
                {
                    "name": "Medication name",
                    "dosage": "Dosage amount",
                    "frequency": "How often",
                    "duration": "Treatment duration",
                    "notes": "Additional notes"
                }
            ],
            "lifestyle_advice": [
                "Lifestyle recommendation 1",
                "Lifestyle recommendation 2"
            ],
            "follow_up_recommendations": "Follow-up guidance",
            "additional_notes": "Any additional important notes"
        }
        
        CONFIDENCE SCORING:
        - 0.9-1.0: Very high confidence (clear, classic presentation)
        - 0.7-0.89: High confidence (typical presentation)
        - 0.5-0.69: Moderate confidence (some uncertainty)
        - 0.3-0.49: Low confidence (multiple possibilities)
        - 0.1-0.29: Very low confidence (insufficient information)
        
        MEDICATION SAFETY:
        - Only suggest FDA-approved medications
        - Include appropriate warnings
        - Consider drug interactions
        - Recommend consulting healthcare provider
        
        Remember: This is an AI-generated diagnosis and should complement, not replace, professional medical evaluation.'''

    async def health_check(self) -> bool:
        """Check if OpenAI service is healthy."""
        try:
            # Simple test call to verify API connectivity
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello",
                    }
                ],
                max_tokens=5,
                temperature=0,
            )
            return bool(response.choices)
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return False


# Global OpenAI service instance
openai_service = OpenAIService()
