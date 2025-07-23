"""PDF generation service for medical diagnosis reports."""

import base64
from datetime import datetime
from io import BytesIO
from typing import Optional, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

from app.models.structured_response import StructuredDiagnosisResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DiagnosisPDFService:
    """Service for generating professional medical diagnosis PDF reports."""
    
    def __init__(self):
        """Initialize PDF service with custom styles."""
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles for medical reports."""
        # Medical report title
        self.styles.add(ParagraphStyle(
            name='MedicalTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.darkblue
        ))
        
        # Section headers
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            fontName='Helvetica-Bold',
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.darkred,
            borderWidth=0,
            borderColor=colors.darkred,
            borderPadding=2
        ))
        
        # Patient info style
        self.styles.add(ParagraphStyle(
            name='PatientInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica',
            spaceBefore=3,
            spaceAfter=3
        ))
        
        # Diagnosis content
        self.styles.add(ParagraphStyle(
            name='DiagnosisContent',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceBefore=3,
            spaceAfter=3,
            alignment=TA_JUSTIFY
        ))
        
        # Warning/Important text
        self.styles.add(ParagraphStyle(
            name='WarningText',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            textColor=colors.red,
            spaceBefore=5,
            spaceAfter=5
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName='Helvetica',
            alignment=TA_CENTER,
            textColor=colors.grey
        ))
    
    async def generate_diagnosis_pdf(
        self,
        diagnosis_data: StructuredDiagnosisResponse,
        doctor_notes: Optional[str] = None,
        clinic_info: Optional[dict] = None
    ) -> BytesIO:
        """
        Generate a professional PDF report for medical diagnosis.
        
        Args:
            diagnosis_data: Structured diagnosis response data
            doctor_notes: Additional notes from the reviewing doctor
            clinic_info: Clinic/hospital information for header
            
        Returns:
            BytesIO: PDF file as bytes
        """
        try:
            logger.info(f"Generating PDF for diagnosis request: {diagnosis_data.request_id}")
            
            # Create PDF buffer
            buffer = BytesIO()
            
            # Create document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build document content
            story = []
            
            # Header
            story.extend(self._build_header(clinic_info))
            
            # Patient Information
            story.extend(self._build_patient_info(diagnosis_data))
            
            # Primary Diagnosis
            story.extend(self._build_diagnosis_section(diagnosis_data))
            
            # Clinical Reasoning
            story.extend(self._build_clinical_reasoning(diagnosis_data))
            
            # Safety Assessment
            story.extend(self._build_safety_assessment(diagnosis_data))
            
            # Investigations
            story.extend(self._build_investigations(diagnosis_data))
            
            # Treatment Recommendations
            story.extend(self._build_treatment_recommendations(diagnosis_data))
            
            # Patient Education
            story.extend(self._build_patient_education(diagnosis_data))
            
            # Doctor's Additional Notes
            if doctor_notes:
                story.extend(self._build_doctor_notes(doctor_notes))
            
            # Footer/Disclaimer
            story.extend(self._build_footer(diagnosis_data))
            
            # Build PDF
            doc.build(story)
            
            # Return buffer
            buffer.seek(0)
            logger.info(f"PDF generated successfully for request: {diagnosis_data.request_id}")
            return buffer
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise
    
    def _build_header(self, clinic_info: Optional[dict]) -> List:
        """Build PDF header section."""
        story = []
        
        # Clinic/Hospital Name
        if clinic_info and clinic_info.get('name'):
            story.append(Paragraph(clinic_info['name'], self.styles['MedicalTitle']))
            if clinic_info.get('address'):
                story.append(Paragraph(clinic_info['address'], self.styles['PatientInfo']))
            story.append(Spacer(1, 12))
        
        # Report Title
        story.append(Paragraph("AI-ASSISTED GYNECOLOGICAL DIAGNOSIS REPORT", self.styles['MedicalTitle']))
        story.append(Spacer(1, 20))
        
        return story
    
    def _build_patient_info(self, diagnosis_data: StructuredDiagnosisResponse) -> List:
        """Build patient information section."""
        story = []
        
        story.append(Paragraph("PATIENT INFORMATION", self.styles['SectionHeader']))
        
        # Patient info table
        patient_data = [
            ['Request ID:', diagnosis_data.request_id],
            ['Patient Age:', f"{diagnosis_data.patient_age} years"],
            ['Primary Symptom:', diagnosis_data.primary_symptom.replace('_', ' ').title()],
            ['Report Generated:', datetime.now().strftime("%B %d, %Y at %I:%M %p")],
        ]
        
        patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        
        story.append(patient_table)
        story.append(Spacer(1, 15))
        
        return story
    
    def _build_diagnosis_section(self, diagnosis_data: StructuredDiagnosisResponse) -> List:
        """Build diagnosis section."""
        story = []
        
        story.append(Paragraph("DIFFERENTIAL DIAGNOSIS", self.styles['SectionHeader']))
        
        # Diagnosis table
        diagnosis_data_table = [['Diagnosis', 'Confidence', 'Description']]
        
        for diag in diagnosis_data.possible_diagnoses:
            confidence_str = f"{diag.confidence_score:.1%}"
            description = diag.description or "Clinical assessment based on presented symptoms"
            diagnosis_data_table.append([
                diag.name,
                confidence_str,
                description
            ])
        
        diag_table = Table(diagnosis_data_table, colWidths=[2.5*inch, 1*inch, 2.5*inch])
        diag_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ]))
        
        story.append(diag_table)
        story.append(Spacer(1, 15))
        
        return story
    
    def _build_clinical_reasoning(self, diagnosis_data: StructuredDiagnosisResponse) -> List:
        """Build clinical reasoning section."""
        story = []
        
        story.append(Paragraph("CLINICAL REASONING", self.styles['SectionHeader']))
        story.append(Paragraph(diagnosis_data.clinical_reasoning, self.styles['DiagnosisContent']))
        
        if diagnosis_data.differential_considerations:
            story.append(Paragraph("<b>Differential Considerations:</b>", self.styles['DiagnosisContent']))
            for consideration in diagnosis_data.differential_considerations:
                story.append(Paragraph(f"• {consideration}", self.styles['DiagnosisContent']))
        
        story.append(Spacer(1, 15))
        return story
    
    def _build_safety_assessment(self, diagnosis_data: StructuredDiagnosisResponse) -> List:
        """Build safety assessment section."""
        story = []
        
        story.append(Paragraph("SAFETY ASSESSMENT", self.styles['SectionHeader']))
        
        # Allergy information
        if diagnosis_data.safety_assessment.allergy_considerations.allergic_medications:
            story.append(Paragraph("<b>Known Drug Allergies:</b>", self.styles['WarningText']))
            allergies = ", ".join(diagnosis_data.safety_assessment.allergy_considerations.allergic_medications)
            story.append(Paragraph(allergies, self.styles['WarningText']))
        
        # Safety warnings
        if diagnosis_data.safety_assessment.safety_warnings:
            story.append(Paragraph("<b>Safety Warnings:</b>", self.styles['DiagnosisContent']))
            for warning in diagnosis_data.safety_assessment.safety_warnings:
                story.append(Paragraph(f"• {warning}", self.styles['DiagnosisContent']))
        
        # Risk assessment
        urgency_color = colors.green if diagnosis_data.risk_assessment.urgency_level == 'low' else colors.orange
        if diagnosis_data.risk_assessment.urgency_level == 'urgent':
            urgency_color = colors.red
            
        story.append(Paragraph(
            f"<b>Urgency Level: {diagnosis_data.risk_assessment.urgency_level.upper()}</b>",
            ParagraphStyle(
                'UrgencyLevel',
                parent=self.styles['DiagnosisContent'],
                textColor=urgency_color,
                fontName='Helvetica-Bold'
            )
        ))
        
        story.append(Spacer(1, 15))
        return story
    
    def _build_investigations(self, diagnosis_data: StructuredDiagnosisResponse) -> List:
        """Build investigations section."""
        story = []
        
        if diagnosis_data.recommended_investigations:
            story.append(Paragraph("RECOMMENDED INVESTIGATIONS", self.styles['SectionHeader']))
            
            inv_data = [['Investigation', 'Priority', 'Reason']]
            for inv in diagnosis_data.recommended_investigations:
                inv_data.append([inv.name, inv.priority.title(), inv.reason])
            
            inv_table = Table(inv_data, colWidths=[2*inch, 1*inch, 3*inch])
            inv_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ]))
            
            story.append(inv_table)
            story.append(Spacer(1, 15))
        
        return story
    
    def _build_treatment_recommendations(self, diagnosis_data: StructuredDiagnosisResponse) -> List:
        """Build treatment recommendations section."""
        story = []
        
        story.append(Paragraph("TREATMENT RECOMMENDATIONS", self.styles['SectionHeader']))
        
        # Primary treatment
        if diagnosis_data.treatment_recommendations.primary_treatment:
            story.append(Paragraph(
                f"<b>Primary Treatment:</b> {diagnosis_data.treatment_recommendations.primary_treatment}",
                self.styles['DiagnosisContent']
            ))
        
        # Medications
        if diagnosis_data.treatment_recommendations.safe_medications:
            story.append(Paragraph("<b>Recommended Medications:</b>", self.styles['DiagnosisContent']))
            
            med_data = [['Medication', 'Dosage', 'Frequency', 'Duration', 'Notes']]
            for med in diagnosis_data.treatment_recommendations.safe_medications:
                med_data.append([
                    med.name,
                    med.dosage,
                    med.frequency,
                    med.duration,
                    med.notes or med.reason
                ])
            
            med_table = Table(med_data, colWidths=[1.2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 2.4*inch])
            med_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightyellow),
            ]))
            
            story.append(med_table)
        
        # Lifestyle modifications
        if diagnosis_data.treatment_recommendations.lifestyle_modifications:
            story.append(Paragraph("<b>Lifestyle Modifications:</b>", self.styles['DiagnosisContent']))
            for modification in diagnosis_data.treatment_recommendations.lifestyle_modifications:
                story.append(Paragraph(f"• {modification}", self.styles['DiagnosisContent']))
        
        story.append(Spacer(1, 15))
        return story
    
    def _build_patient_education(self, diagnosis_data: StructuredDiagnosisResponse) -> List:
        """Build patient education section."""
        story = []
        
        if diagnosis_data.patient_education:
            story.append(Paragraph("PATIENT EDUCATION", self.styles['SectionHeader']))
            for education in diagnosis_data.patient_education:
                story.append(Paragraph(f"• {education}", self.styles['DiagnosisContent']))
            story.append(Spacer(1, 15))
        
        # Warning signs
        if diagnosis_data.warning_signs:
            story.append(Paragraph("WARNING SIGNS - SEEK IMMEDIATE MEDICAL ATTENTION", self.styles['WarningText']))
            for warning in diagnosis_data.warning_signs:
                story.append(Paragraph(f"• {warning}", self.styles['WarningText']))
            story.append(Spacer(1, 15))
        
        return story
    
    def _build_doctor_notes(self, doctor_notes: str) -> List:
        """Build doctor's additional notes section."""
        story = []
        
        story.append(Paragraph("DOCTOR'S ADDITIONAL NOTES", self.styles['SectionHeader']))
        story.append(Paragraph(doctor_notes, self.styles['DiagnosisContent']))
        story.append(Spacer(1, 15))
        
        return story
    
    def _build_footer(self, diagnosis_data: StructuredDiagnosisResponse) -> List:
        """Build footer with disclaimer."""
        story = []
        
        story.append(Spacer(1, 20))
        story.append(Paragraph("MEDICAL DISCLAIMER", self.styles['SectionHeader']))
        story.append(Paragraph(diagnosis_data.disclaimer, self.styles['DiagnosisContent']))
        
        # Confidence score
        story.append(Paragraph(
            f"<b>Overall AI Confidence Score: {diagnosis_data.confidence_score:.1%}</b>",
            self.styles['DiagnosisContent']
        ))
        
        # Generation timestamp
        story.append(Paragraph(
            f"Report generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Footer']
        ))
        
        return story


# Global PDF service instance
pdf_service = DiagnosisPDFService()
