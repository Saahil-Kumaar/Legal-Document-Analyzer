import json
import streamlit as st
from datetime import datetime

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
