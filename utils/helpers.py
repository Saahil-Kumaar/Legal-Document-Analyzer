import json
import streamlit as st
from datetime import datetime

# def load_config():
#     """Load configuration from Streamlit secrets"""
#     return {
#         'firebase': dict(st.secrets['firebase']),
#         'project_id': st.secrets['google_cloud']['project_id'],
#         'location': st.secrets['google_cloud']['location']
#     }
def load_config():
    """Load configuration from Streamlit secrets"""
    try:
        return {
            'firebase': dict(st.secrets['firebase']),
            'project_id': st.secrets['google_cloud']['project_id'],
            'location': st.secrets['google_cloud']['location']
        }
    except KeyError as e:
        st.error(f"Missing configuration in secrets: {e}")
        st.error("Please ensure firebase and google_cloud sections are properly configured in secrets.toml")
        st.stop()


def save_analysis_history(user_id: str, analysis: dict):
    """Save analysis to user history"""
    # Implementation for saving to Firebase
    pass

def export_analysis_pdf(analysis: dict) -> bytes:
    """Export analysis as PDF"""
    # Implementation for PDF generation
    pass

def calculate_risk_score(analysis: dict) -> int:
    """Calculate overall risk score (1-10)"""
    risks = analysis.get('risks', [])
    if not risks:
        return 1
    return min(10, max(1, len(risks) * 2))

# import json
# import streamlit as st
# from datetime import datetime
# from fpdf import FPDF
# import firebase_admin
# from firebase_admin import credentials, firestore

# # Initialize Firebase Admin SDK
# firebase_config = st.secrets['firebase']
# cred = credentials.Certificate(firebase_config)
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# def load_config():
#     """Load configuration from Streamlit secrets"""
#     return {
#         'firebase': dict(st.secrets['firebase']),
#         'project_id': st.secrets['google_cloud']['project_id'],
#         'location': st.secrets['google_cloud']['location']
#     }

# def save_analysis_history(user_id: str, analysis: dict):
#     """Save analysis to user history"""
#     timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     analysis['timestamp'] = timestamp
#     try:
#         db.collection('users').document(user_id).collection('analysis_history').add(analysis)
#         st.success('Analysis saved successfully.')
#     except Exception as e:
#         st.error(f'Failed to save analysis: {e}')

# def export_analysis_pdf(analysis: dict) -> bytes:
#     """Export analysis as PDF"""
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
    
#     pdf.cell(200, 10, txt="Analysis Report", ln=True, align='C')
#     pdf.cell(200, 10, txt=f"Timestamp: {analysis.get('timestamp', 'N/A')}", ln=True)
    
#     for key, value in analysis.items():
#         pdf.cell(200, 10, txt=f"{key.capitalize()}: {value}", ln=True)
    
#     return pdf.output(dest='S')

# def calculate_risk_score(analysis: dict) -> int:
#     """Calculate overall risk score (1-10)"""
#     risks = analysis.get('risks', [])
#     if not risks:
#         return 1
#     return min(10, max(1, len(risks) * 2))
