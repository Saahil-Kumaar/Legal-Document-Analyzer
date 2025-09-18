import streamlit as st
from streamlit_option_menu import option_menu
from auth.firebase_auth import FirebaseAuth
from ai.gemini_client import GeminiProcessor
from ai.document_processor import DocumentProcessor
from utils.helpers import load_config

def main():
    st.set_page_config(
        page_title="Legal Document Analyzer",
        page_icon="⚖️"
    )
    
    # Load configuration
    config = load_config()
    
    # Initialize services
    if 'firebase_auth' not in st.session_state:
        st.session_state.firebase_auth = FirebaseAuth(config['firebase'])
    # if 'gemini_processor' not in st.session_state:
    #     st.session_state.gemini_processor = GeminiProcessor(config['project_id'])
    if 'gemini_processor' not in st.session_state:
        try:
            st.session_state.gemini_processor = GeminiProcessor(
                config['project_id'], 
                config['location']
            )
        except Exception as e:
            st.error(f"Failed to initialize Gemini processor: {e}")
            st.error("Please check your Google Cloud credentials in secrets.toml")
            st.stop()

    
    # Authentication flow
    if 'user' not in st.session_state:
        show_auth_page()
    else:
        show_main_app()

def show_auth_page():
    """Display login/signup interface"""
    st.title("⚖️ Legal Document Analyzer")
    st.subheader("Simplify Complex Legal Documents with AI")
    
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
    
    with tab1:
        with st.form("signin_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")
            
            if submit:
                user = st.session_state.firebase_auth.sign_in(email, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
    
    with tab2:
        with st.form("signup_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Sign Up")
            
            if submit:
                if password == confirm_password:
                    if st.session_state.firebase_auth.sign_up(email, password, username):
                        st.success("Account created successfully! Please sign in.")
                else:
                    st.error("Passwords don't match!")

def show_main_app():
    """Main application interface"""
    st.sidebar.title(f"Welcome, {st.session_state.user.get('email', 'User')}")
    # st.sidebar.title(f"Welcome, {auth.get_user_by_email(email)}")
    
    if st.sidebar.button("Sign Out"):
        del st.session_state.user
        st.rerun()
    
    st.title("⚖️ Legal Document Analyzer")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📄 Upload Your Legal Document")
        uploaded_file = st.file_uploader(
            "Choose a document", 
            type=['pdf', 'docx'],
            help="Upload PDF or DOCX legal documents"
        )
        
        if uploaded_file:
            process_document(uploaded_file)
    
    with col2:
        st.subheader("💬 Ask Questions")
        if 'document_analysis' in st.session_state:
            show_chat_interface()

def process_document(uploaded_file):
    """Process uploaded document"""
    try:
        with st.spinner("Analyzing document..."):
            # Extract text
            if uploaded_file.type == "application/pdf":
                text = DocumentProcessor.extract_text_from_pdf(uploaded_file)
            else:
                text = DocumentProcessor.extract_text_from_docx(uploaded_file)
            
            # Analyze with AI
            analysis = st.session_state.gemini_processor.analyze_document(text)
            st.session_state.document_analysis = analysis
            st.session_state.document_text = text
            
            # Display results
            display_analysis(analysis)
            
    except Exception as e:
        st.error(f"Error processing document: {e}")

def display_analysis(analysis):
    """Display document analysis results"""
    # Summary
    st.subheader("**📝 Document Summary**")
    st.markdown(analysis.get('summary', 'No summary available')) 

    #Tab Cretion
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(["Key Terms", "Main Clauses", "Risks", "Recommendations","Parties", "Jurisdictions", "Obligations", "Critical Dates", "Missing/Unusual", "Compliance Issues", "Next Steps"])
    
    # Key Terms
    with tab1:
        if 'key_terms' in analysis:
            st.subheader("**🔑 Key Terms:**")
            for term in analysis['key_terms']:
                st.success(f"• **{term}**")

    # Main Clauses
    with tab2:
        if 'main_clauses' in analysis:
            st.subheader("**📋 Main Clauses:**")
            for i, clause in enumerate(analysis['main_clauses'], 1):
                st.warning(f"{i}. {clause}")
    
    # Risks
    with tab3:
        if 'risks' in analysis:
            st.subheader("**⚠️ Potential Risks:**")
            for risk in analysis['risks']:
                st.error(risk)
    
    # Recommendations
    with tab4:
        if 'recommendations' in analysis:
            st.subheader("**💡 Recommendations:**")
            for rec in analysis['recommendations']:
                st.info(rec)

    # Parties
    with tab5:
        if 'parties' in analysis:
            st.subheader("**👥 Parties:**")
            for party in analysis['parties']:
                st.success(party)

    # Jurisdiction
    with tab6:
        if 'jurisdiction' in analysis:
            st.subheader("**⚖️ Jurisdiction:**")
            st.warning(analysis['jurisdiction'])

    # Obligations
    with tab7:
        if 'obligations' in analysis:
            st.subheader("**📌 Obligations:**")
            for obligation in analysis['obligations']:
                st.error(obligation)

    # Critical Dates
    with tab8:
        if 'critical_dates' in analysis:
            st.subheader("**📅 Critical Dates:**")
            for date in analysis['critical_dates']:
                st.info(date)

    # Missing or Unusual Clauses
    with tab9:
        if 'missing_or_unusual' in analysis:
            st.subheader("**❗ Missing or Unusual Clauses:**")
            for clause in analysis['missing_or_unusual']:
                st.success(clause)

    # Compliance Issues
    with tab10:
        if 'compliance_issues' in analysis:
            st.subheader("**🛑 Compliance Issues:**")
            for issue in analysis['compliance_issues']:
                st.warning(issue)

    # Next Steps
    with tab11:
        if 'next_steps' in analysis:
            st.subheader("**➡️ Next Steps:**")
            for step in analysis['next_steps']:
                st.error(step)


def show_chat_interface():
    """Interactive chat about the document"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['question']}")
        st.write(f"**AI:** {chat['answer']}")
        st.write("---")
    
    # Chat input
    question = st.text_input("Ask about your document:", key="chat_input")
    if st.button("Ask") and question:
        answer = st.session_state.gemini_processor.chat_about_document(
            question, st.session_state.document_text
        )
        st.session_state.chat_history.append({
            'question': question,
            'answer': answer
        })
        st.rerun()

if __name__ == "__main__":
    main()



