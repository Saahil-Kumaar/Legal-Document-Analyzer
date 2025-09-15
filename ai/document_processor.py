# ai/document_processor.py
import PyPDF2
import docx
from typing import Optional

class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(file) -> str:
        """Extract text from uploaded PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")
    
    @staticmethod
    def extract_text_from_docx(file) -> str:
        """Extract text from uploaded DOCX"""
        try:
            doc = docx.Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {e}")
    
    @staticmethod
    def identify_document_type(text: str) -> str:
        """Identify the type of legal document"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['lease', 'tenant', 'landlord', 'rent']):
            return "rental_agreement"
        elif any(term in text_lower for term in ['loan', 'borrower', 'lender', 'principal']):
            return "loan_contract"
        elif any(term in text_lower for term in ['terms of service', 'privacy policy', 'user agreement']):
            return "terms_of_service"
        elif any(term in text_lower for term in ['employment', 'employee', 'employer']):
            return "employment_contract"
        else:
            return "general_legal"
