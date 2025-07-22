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
        onset: Optional[str] = None,
        progression: Optional[str] = None,
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

    async def generate_structured_diagnosis(
        self,
        request: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate comprehensive AI diagnosis based on structured patient data.
        
        Args:
            request: Structured diagnosis request data
            
        Returns:
            Dict containing comprehensive diagnosis information
            
        Raises:
            OpenAIServiceError: If OpenAI API call fails
        """
        try:
            prompt = self._create_structured_diagnosis_prompt(request)

            logger.info(f"Generating structured diagnosis for request ID {request.get('patient_profile', {}).get('request_id', 'unknown')}")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_structured_system_prompt(),
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
            
            logger.info(f"Successfully generated structured diagnosis with {len(diagnosis_data.get('possible_diagnoses', []))} possible diagnoses")
            
            return diagnosis_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI structured response as JSON: {e}")
            raise OpenAIServiceError(f"Invalid JSON response from OpenAI: {e}")
        except Exception as e:
            logger.error(f"Structured OpenAI API call failed: {e}")
            raise OpenAIServiceError(f"Structured OpenAI API call failed: {e}")

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

    def _create_structured_diagnosis_prompt(self, request: Dict[str, Any]) -> str:
        """Create structured diagnosis prompt for OpenAI."""
        patient_profile = request.get('patient_profile', {})
        primary_complaint = request.get('primary_complaint', {})
        symptom_details = request.get('symptom_specific_details', {})
        reproductive_history = request.get('reproductive_history', {})
        associated_symptoms = request.get('associated_symptoms', {})
        medical_context = request.get('medical_context', {})
        healthcare_interaction = request.get('healthcare_interaction', {})
        patient_concerns = request.get('patient_concerns', {})

        prompt_parts = [
            "=== COMPREHENSIVE PATIENT ASSESSMENT ===",
            "",
            "PATIENT PROFILE:",
            f"- Age: {patient_profile.get('age')} years",
            f"- Request ID: {patient_profile.get('request_id')}",
            f"- Timestamp: {patient_profile.get('timestamp')}",
            "",
            "PRIMARY COMPLAINT:",
            f"- Main Symptom: {primary_complaint.get('main_symptom')}",
            f"- Duration: {primary_complaint.get('duration')}",
            f"- Severity: {primary_complaint.get('severity')}",
            f"- Onset: {primary_complaint.get('onset')}",
            f"- Progression: {primary_complaint.get('progression')}",
            "",
        ]

        # Add symptom-specific details
        if symptom_details:
            prompt_parts.append("SYMPTOM-SPECIFIC DETAILS:")
            for key, value in symptom_details.items():
                if isinstance(value, dict):
                    prompt_parts.append(f"- {key.title()}:")
                    for sub_key, sub_value in value.items():
                        prompt_parts.append(f"  • {sub_key.replace('_', ' ').title()}: {sub_value}")
                else:
                    prompt_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
            prompt_parts.append("")

        # Add reproductive history
        if reproductive_history:
            prompt_parts.append("REPRODUCTIVE HISTORY:")
            for section, data in reproductive_history.items():
                prompt_parts.append(f"- {section.replace('_', ' ').title()}:")
                if isinstance(data, dict):
                    for key, value in data.items():
                        prompt_parts.append(f"  • {key.replace('_', ' ').title()}: {value}")
            prompt_parts.append("")

        # Add associated symptoms
        if associated_symptoms:
            prompt_parts.append("ASSOCIATED SYMPTOMS:")
            for category, symptoms in associated_symptoms.items():
                prompt_parts.append(f"- {category.title()} Symptoms:")
                if isinstance(symptoms, dict):
                    for symptom, severity in symptoms.items():
                        prompt_parts.append(f"  • {symptom.replace('_', ' ').title()}: {severity}")
            prompt_parts.append("")

        # Add medical context
        if medical_context:
            prompt_parts.append("MEDICAL CONTEXT:")
            for key, value in medical_context.items():
                if isinstance(value, list) and value:
                    prompt_parts.append(f"- {key.replace('_', ' ').title()}: {', '.join(value)}")
                elif value:
                    prompt_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
            prompt_parts.append("")

        # Add healthcare interaction
        if healthcare_interaction:
            prompt_parts.append("HEALTHCARE INTERACTION:")
            for key, value in healthcare_interaction.items():
                if value:
                    prompt_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
            prompt_parts.append("")

        # Add patient concerns
        if patient_concerns:
            prompt_parts.append("PATIENT CONCERNS:")
            for key, value in patient_concerns.items():
                if value:
                    prompt_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
            prompt_parts.append("")

        prompt_parts.extend([
            "=== CLINICAL ANALYSIS REQUEST ===",
            "",
            "Please provide a comprehensive gynecological analysis based on the above information.",
            "Pay special attention to:",
            "1. Drug allergies and contraindications",
            "2. Existing medical conditions and their impact",
            "3. Symptom pattern analysis and differential diagnosis",
            "4. Risk assessment and urgency level",
            "5. Safe treatment alternatives considering allergies",
            "6. Patient education and safety warnings",
            "",
            "Focus on evidence-based medicine and patient safety.",
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

    def _get_structured_system_prompt(self) -> str:
        """Get structured system prompt for comprehensive diagnosis."""
        return '''You are an advanced AI assistant specialized in comprehensive gynecological diagnosis and treatment planning.
        
        Your task is to analyze detailed patient information and provide a thorough, structured medical assessment.
        
        CRITICAL REQUIREMENTS:
        1. SAFETY FIRST: Always check for drug allergies and contraindications
        2. EVIDENCE-BASED: Base all recommendations on current medical guidelines
        3. COMPREHENSIVE: Address all aspects of the patient's presentation
        4. PATIENT-CENTERED: Consider patient concerns and quality of life
        5. CONSERVATIVE: Err on the side of caution in recommendations
        
        RESPONSE FORMAT:
        You must respond with a valid JSON object containing:
        {
            "possible_diagnoses": [
                {
                    "name": "Diagnosis name",
                    "confidence_score": 0.85,
                    "description": "Brief clinical description"
                }
            ],
            "clinical_reasoning": "Detailed clinical reasoning behind the primary diagnosis",
            "differential_considerations": [
                "Alternative diagnosis consideration 1",
                "Alternative diagnosis consideration 2"
            ],
            "safety_assessment": {
                "allergy_considerations": {
                    "allergic_medications": ["drug1", "drug2"],
                    "safe_alternatives": ["safe drug1", "safe drug2"],
                    "contraindicated_drugs": ["avoid drug1", "avoid drug2"]
                },
                "condition_interactions": ["interaction1", "interaction2"],
                "safety_warnings": ["warning1", "warning2"]
            },
            "risk_assessment": {
                "urgency_level": "low/moderate/high/urgent",
                "red_flags": ["red flag1", "red flag2"],
                "when_to_seek_emergency_care": ["emergency sign1", "emergency sign2"]
            },
            "recommended_investigations": [
                {
                    "name": "Test name",
                    "priority": "low/medium/high",
                    "reason": "Reason for test"
                }
            ],
            "treatment_recommendations": {
                "primary_treatment": "Primary treatment approach",
                "safe_medications": [
                    {
                        "name": "Medication name",
                        "dosage": "Dosage",
                        "frequency": "How often",
                        "duration": "Duration",
                        "reason": "Reason for prescribing",
                        "notes": "Safety notes"
                    }
                ],
                "lifestyle_modifications": ["modification1", "modification2"],
                "dietary_advice": ["dietary advice1", "dietary advice2"],
                "follow_up_timeline": "Follow-up recommendations"
            },
            "patient_education": [
                "education point 1",
                "education point 2"
            ],
            "warning_signs": [
                "warning sign 1",
                "warning sign 2"
            ],
            "confidence_score": 0.85,
            "processing_notes": [
                "note about allergy considerations",
                "note about complexity"
            ]
        }
        
        SPECIAL CONSIDERATIONS:
        - Drug Allergies: NEVER recommend medications patient is allergic to
        - Multiple Allergies: Focus on topical treatments and safe alternatives
        - Diabetes: Consider impact on infection risk and medication metabolism
        - Previous Failed Treatments: Suggest different therapeutic approaches
        
        CONFIDENCE SCORING:
        - 0.9-1.0: Clear, textbook presentation with definitive indicators
        - 0.7-0.89: Strong clinical indicators with minor uncertainties
        - 0.5-0.69: Probable diagnosis with some competing possibilities
        - 0.3-0.49: Uncertain diagnosis requiring further investigation
        - 0.1-0.29: Multiple possibilities, insufficient discriminating features
        
        URGENCY LEVELS:
        - "urgent": Immediate medical attention required (same day)
        - "high": See healthcare provider within 24-48 hours
        - "moderate": Schedule appointment within 1-2 weeks
        - "low": Routine follow-up or self-care management
        
        Remember: This comprehensive assessment should guide clinical decision-making but never replace professional medical evaluation and patient-provider relationship.'''

    async def generate_new_structured_diagnosis(
        self,
        request: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate diagnosis using the new structured format.
        
        Args:
            request: New structured diagnosis request data
            
        Returns:
            Dict containing diagnosis information in new format
            
        Raises:
            OpenAIServiceError: If OpenAI API call fails
        """
        try:
            prompt = self._create_new_structured_diagnosis_prompt(request)

            logger.info(f"Generating new structured diagnosis for request ID {request.get('patient_profile', {}).get('request_id', 'unknown')}")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_new_structured_system_prompt(),
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
            
            logger.info(f"Successfully generated new structured diagnosis: {diagnosis_data.get('diagnosis', 'Unknown')}")
            
            return diagnosis_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI new structured response as JSON: {e}")
            raise OpenAIServiceError(f"Invalid JSON response from OpenAI: {e}")
        except Exception as e:
            logger.error(f"New structured OpenAI API call failed: {e}")
            raise OpenAIServiceError(f"New structured OpenAI API call failed: {e}")

    def _create_new_structured_diagnosis_prompt(self, request: Dict[str, Any]) -> str:
        """Create new structured diagnosis prompt for OpenAI."""
        patient_profile = request.get('patient_profile', {})
        primary_complaint = request.get('primary_complaint', {})
        symptom_details = request.get('symptom_specific_details', {})
        reproductive_history = request.get('reproductive_history', {})
        associated_symptoms = request.get('associated_symptoms', {})
        medical_context = request.get('medical_context', {})
        healthcare_interaction = request.get('healthcare_interaction', {})
        patient_concerns = request.get('patient_concerns', {})

        prompt_parts = [
            "=== COMPREHENSIVE PATIENT ASSESSMENT ===",
            "",
            "PATIENT PROFILE:",
            f"- Age: {patient_profile.get('age')} years",
            f"- Request ID: {patient_profile.get('request_id')}",
            f"- Timestamp: {patient_profile.get('timestamp')}",
            "",
            "PRIMARY COMPLAINT:",
            f"- Main Symptom: {primary_complaint.get('main_symptom')}",
            f"- Duration: {primary_complaint.get('duration')}",
            f"- Severity: {primary_complaint.get('severity')}",
            f"- Onset: {primary_complaint.get('onset')}",
            f"- Progression: {primary_complaint.get('progression')}",
            "",
        ]

        # Add symptom-specific details
        if symptom_details:
            prompt_parts.append("SYMPTOM-SPECIFIC DETAILS:")
            for key, value in symptom_details.items():
                if isinstance(value, dict):
                    prompt_parts.append(f"- {key.title()}:")
                    for sub_key, sub_value in value.items():
                        prompt_parts.append(f"  • {sub_key.replace('_', ' ').title()}: {sub_value}")
                else:
                    prompt_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
            prompt_parts.append("")

        # Add reproductive history
        if reproductive_history:
            prompt_parts.append("REPRODUCTIVE HISTORY:")
            for section, data in reproductive_history.items():
                prompt_parts.append(f"- {section.replace('_', ' ').title()}:")
                if isinstance(data, dict):
                    for key, value in data.items():
                        prompt_parts.append(f"  • {key.replace('_', ' ').title()}: {value}")
            prompt_parts.append("")

        # Add associated symptoms
        if associated_symptoms:
            prompt_parts.append("ASSOCIATED SYMPTOMS:")
            for category, symptoms in associated_symptoms.items():
                prompt_parts.append(f"- {category.title()} Symptoms:")
                if isinstance(symptoms, dict):
                    for symptom, severity in symptoms.items():
                        prompt_parts.append(f"  • {symptom.replace('_', ' ').title()}: {severity}")
            prompt_parts.append("")

        # Add medical context
        if medical_context:
            prompt_parts.append("MEDICAL CONTEXT:")
            for key, value in medical_context.items():
                if isinstance(value, list) and value:
                    prompt_parts.append(f"- {key.replace('_', ' ').title()}: {', '.join(value)}")
                elif value:
                    prompt_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
            prompt_parts.append("")

        # Add healthcare interaction
        if healthcare_interaction:
            prompt_parts.append("HEALTHCARE INTERACTION:")
            for key, value in healthcare_interaction.items():
                if value:
                    prompt_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
            prompt_parts.append("")

        # Add patient concerns
        if patient_concerns:
            prompt_parts.append("PATIENT CONCERNS:")
            for key, value in patient_concerns.items():
                if value:
                    prompt_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
            prompt_parts.append("")

        prompt_parts.extend([
            "=== CLINICAL ANALYSIS REQUEST ===",
            "",
            "Please provide a comprehensive gynecological diagnosis based on the above information.",
            "Pay special attention to:",
            "1. Drug allergies and contraindications",
            "2. Existing medical conditions and their impact",
            "3. Symptom pattern analysis and differential diagnosis",
            "4. Patient safety and appropriate treatment options",
            "",
            "Focus on evidence-based medicine and patient safety.",
        ])

        return "\n".join(prompt_parts)

    def _get_new_structured_system_prompt(self) -> str:
        """Get system prompt for new structured diagnosis."""
        return '''You are a specialized AI assistant for gynecological diagnosis and treatment planning.
        
        Your task is to analyze comprehensive patient information and provide a structured medical assessment.
        
        CRITICAL REQUIREMENTS:
        1. SAFETY FIRST: Always check for drug allergies and contraindications
        2. EVIDENCE-BASED: Base all recommendations on current medical guidelines
        3. COMPREHENSIVE: Address all aspects of the patient's presentation
        4. PATIENT-CENTERED: Consider patient concerns and quality of life
        5. CONSERVATIVE: Err on the side of caution in recommendations
        
        RESPONSE FORMAT:
        You must respond with a valid JSON object containing:
        {
            "diagnosis": "Primary medical diagnosis",
            "confidence_score": 0.85,
            "suggested_investigations": [
                {
                    "name": "Investigation name",
                    "priority": "high|medium|low",
                    "reason": "Why this test is needed"
                }
            ],
            "recommended_medications": [
                {
                    "name": "Medication name",
                    "dosage": "150mg",
                    "frequency": "Once daily",
                    "duration": "7 days",
                    "reason": "Treatment purpose",
                    "notes": "⚠️ ALLERGY SUBSTITUTION: Replaced [allergic_med] with safe alternative"
                }
            ],
            "lifestyle_advice": [
                "Advice 1",
                "Advice 2"
            ],
            "follow_up_recommendations": "Follow up in 1-2 weeks",
            "disclaimer": "Medical disclaimer text"
        }
        
        SPECIAL CONSIDERATIONS:
        - Drug Allergies: NEVER recommend medications patient is allergic to
        - Multiple Allergies: Focus on topical treatments and safe alternatives
        - Always include allergy substitution notes when applicable
        - Consider diabetes impact on infection risk and medication metabolism
        - Previous failed treatments: Suggest different therapeutic approaches
        
        CONFIDENCE SCORING:
        - 0.9-1.0: Clear, textbook presentation with definitive indicators
        - 0.7-0.89: Strong clinical indicators with minor uncertainties
        - 0.5-0.69: Probable diagnosis with some competing possibilities
        - 0.3-0.49: Uncertain diagnosis requiring further investigation
        - 0.1-0.29: Multiple possibilities, insufficient discriminating features
        
        Remember: This assessment should guide clinical decision-making but never replace professional medical evaluation.'''

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
