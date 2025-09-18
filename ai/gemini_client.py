from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part
import vertexai
import json
import streamlit as st
from google.oauth2 import service_account

class GeminiProcessor:
    # def __init__(self, project_id: str, location: str = "us-central1"):
    #     vertexai.init(project=project_id, location=location)
    #     self.model = GenerativeModel("gemini-2.5-flash")
    def __init__(self, project_id: str, location: str = "us-central1"):    
        credentials = service_account.Credentials.from_service_account_info(st.secrets["firebase"])
        vertexai.init(project=project_id, location=location, credentials=credentials)
        self.model = GenerativeModel("gemini-2.5-flash")

    def analyze_document(self, document_content: str, document_type: str = "legal") -> dict:
        """
        Analyze a legal (or related) document and provide structured insights.
        Returns a dictionary with summary, key terms, clauses, risks,
        recommendations, and critical legal metadata.
        """

        prompt = f"""
        You are an expert legal document analyst reviewing a {document_type}.

        Each field must be filled as defined below:

        1. summary: A 2-3 sentence plain English summary of the document. Avoid legal jargon.  
        2. key_terms: A dictionary of important legal terms or phrases with simple, non-legal definitions(e.g., "Indemnity": "One party promises to cover losses if something goes wrong").  
        3. main_clauses: A list of the main sections/clauses in the document, explained briefly in plain English.  
        4. risks: Any potential risks, unfair obligations, or concerning clauses for the user.  
        5. recommendations: Practical suggestions for what the user should pay attention to or clarify.  
        6. parties: A list naming and briefly describing the main parties involved. If unclear, return [].  
        7. jurisdiction: The governing law or legal jurisdiction. If not found, return "".  
        8. obligations: A list of key duties or actions each party must perform(Do Not search for specific obligations, only general duties or actions).  
        9. critical_dates: Important dates, deadlines, or timeframes mentioned.  
        10. missing_or_unusual: Clauses that are missing, unusual, or raise concerns (e.g., "No termination clause found").  
        11. compliance_issues: Any explicit compliance or regulatory issues (e.g., data privacy, employment law, consumer protection).  
        12. next_steps: Action items or questions the user should ask before agreeing/signing.

        Analyze the document and respond ONLY in valid JSON with these fields:

        {{
        "summary": "2-3 sentence plain English summary (avoid legal jargon).",
        "key_terms": ["term1: definition1", "term2: definition2", ...],
        "main_clauses": ["main clause 1", "main clause 2", ...],
        "risks": ["notable risk 1", "notable risk 2", ...],
        "recommendations": ["practical recommendation 1", "practical recommendation 2", ...],
        "parties": ["Party 1: role", "Party 2: role", ...],
        "jurisdiction": "Legal jurisdiction or governing law, or empty if not stated, ...",
        "obligations": ["**obligor1**: obligation 1", "**obligor2**: obligation 2", ..., "**obligee 1**: obligation 1", "**obligee 2**: obligation 2", ...],
        "critical_dates": ["important date or deadline", ...],
        "missing_or_unusual": ["clause that is missing/unusual", ...],
        "compliance_issues": ["compliance or regulatory concern", ...],
        "next_steps": ["question to ask lawyer", "action before signing"]
        }}

        Rules:
        - If information is not found, return an empty string ("") or empty list ([]).
        - Do not include explanations outside the JSON.
        - Keep responses concise and accessible for non-lawyers.
        - While generating each field, add more and more explanation and context to each field.
        - Strictly return JSON with the specified fields and no additional fields.

        Document: {document_content}
        """

        response = self.model.generate_content(prompt)

        try:
            return self.parse_response(response.text)
        except Exception as e:
            # Fallback in case of invalid JSON
            return {"error": f"Failed to parse response: {str(e)}", "raw": response.text}



    def chat_about_document(self, question: str, document_context: str) -> str:
        """Answer questions about the document"""
        prompt = f"""
        Based on this legal document context, answer the user's question in simple, clear language:
        
        Document Context: {document_context}
        
        User Question: {question}
        
        Provide a helpful, accurate answer that a non-lawyer can understand.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    


    def parse_response(self, response: str) -> dict:
        """Parse the response from Gemini and return a dictionary."""
        try:
            # Check if the response is empty
            if not response.strip():
                st.error("Empty response received from Gemini.")
                return {}
            
            # Debug: Print the response content
            # print("Raw Response:", response)
            
            # Find the first occurrence of the opening curly bracket (`{`)
            start_index = response.find("{")
            if start_index == -1:
                st.error("No valid JSON content found in the response.")
                return {}
            
            # Find the last occurrence of the closing curly bracket (`}`)
            end_index = response.rfind("}")
            if end_index == -1:
                st.error("No closing bracket `}` found in the response.")
                return {}
            
            # Ensure the start_index is before the end_index
            if start_index > end_index:
                st.error("Invalid JSON structure: Start bracket `{` after end bracket `}`.")
                return {}
            
            # Trim the response to include only the valid JSON
            trimmed_response = response[start_index:end_index + 1]
            
            # Debug: Print the trimmed response
            print("Trimmed Response:", trimmed_response)
            
            # Parse the JSON response
            parsed_data = json.loads(trimmed_response)
            return parsed_data
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON: {e}")
            st.error(f"Invalid JSON received: {response}")
            return {}
        except Exception as e:
            st.error(f"Error parsing response: {e}")
            return {}
