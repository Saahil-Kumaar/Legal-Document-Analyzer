# ⚖️ Legal Document Analyzer

A powerful AI-driven web application that simplifies complex legal documents using Google's Gemini AI, making legal text accessible and understandable for everyone.

## 📋 Overview

Legal Document Analyzer is a Streamlit-based web application designed to help users understand complex legal documents through AI-powered analysis. The application breaks down legal jargon into plain English, identifies potential risks, and provides actionable recommendations.

## ✨ Key Features

- **🔐 Secure Authentication**: Firebase-powered user authentication with sign-up and sign-in functionality
- **📄 Multi-Format Support**: Upload and analyze PDF and DOCX legal documents
- **🤖 AI-Powered Analysis**: Advanced document analysis using Google's Gemini 2.5 Flash model
- **📊 Comprehensive Insights**: Detailed breakdown including:
  - Document summary in plain English
  - Key terms and definitions
  - Main clauses identification
  - Risk assessment and alerts
  - Compliance issues detection
  - Critical dates and deadlines
  - Actionable recommendations
- **💬 Interactive Chat**: Ask questions about your uploaded documents
- **🎯 User-Friendly Interface**: Clean, organized tabbed interface for easy navigation

## 🔧 Tech Stack

### Backend
- **Python 3.8+**
- **Streamlit**: Web application framework
- **Google Cloud Vertex AI**: AI model integration
- **Firebase Admin SDK**: Authentication and database
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction

### AI/ML
- **Google Gemini 2.5 Flash**: Document analysis and chat functionality
- **Vertex AI**: Google Cloud AI platform integration

### Authentication & Database
- **Firebase Authentication**: User management
- **Cloud Firestore**: User data storage

## 📁 Project Structure

```
Legal-Document-Analyzer/
├── .streamlit/                # Streamlit configuration
├── ai/                       # AI processing modules
│   ├── document_processor.py # Document text extraction
│   ├── gemini_client.py      # Gemini AI integration
│   └── legal_analyzer.py     # Legal document analysis
├── auth/                     # Authentication modules
│   └── firebase_auth.py      # Firebase authentication handler
├── config/                   # Configuration files
│   └── settings.py           # Application settings
├── utils/                    # Utility functions
│   ├── file_handler.py       # File processing utilities
│   └── helpers.py            # Helper functions and config loader
├── app.py                    # Main Streamlit application
└── requirements.txt          # Project dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Cloud Project with Vertex AI enabled
- Firebase project with Authentication and Firestore enabled

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Saahil-Kumaar/Legal-Document-Analyzer.git
   cd Legal-Document-Analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.streamlit/secrets.toml` file with your configuration:
   ```toml
   [firebase]
   # Your Firebase service account key JSON content
   
   [google_cloud]
   project_id = "your-gcp-project-id"
   location = "us-central1"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📝 Usage

1. **Authentication**: Sign up or sign in using your email and password
2. **Upload Document**: Upload a PDF or DOCX legal document
3. **Review Analysis**: Explore the comprehensive analysis across multiple tabs:
   - **Key Terms**: Important legal terminology with definitions
   - **Main Clauses**: Primary sections of the document
   - **Risks**: Potential concerns and red flags
   - **Recommendations**: Actionable advice
   - **Parties**: Involved entities and their roles
   - **Jurisdictions**: Governing law and legal jurisdiction
   - **Obligations**: Duties and responsibilities
   - **Critical Dates**: Important deadlines and timeframes
4. **Interactive Chat**: Ask specific questions about your document
5. **Risk Assessment**: View calculated risk scores for decision-making

## 🤖 AI Features

The application leverages Google's Gemini 2.5 Flash model to provide:
- **Intelligent Document Parsing**: Extracts and understands legal document structure
- **Plain English Translation**: Converts complex legal language into accessible terms
- **Risk Identification**: Automatically flags potential concerns and unfavorable clauses
- **Contextual Q&A**: Interactive chat functionality for document-specific questions
- **Compliance Monitoring**: Identifies regulatory and legal compliance issues

## 🔒 Security & Privacy

- **Secure Authentication**: Firebase-powered user authentication
- **Data Protection**: User documents and analysis are securely handled
- **Privacy-First**: No permanent storage of sensitive document content
- **Encrypted Communications**: All data transmission is encrypted

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Saahil Kumar**
- GitHub: [@Saahil-Kumaar](https://github.com/Saahil-Kumaar)

## 🙏 Acknowledgments

- Google Cloud Platform for Vertex AI and Gemini models
- Firebase for authentication and database services
- Streamlit for the web application framework
- The open-source community for various libraries and tools

---

**⚠️ Disclaimer**: This tool is designed to assist with document analysis and should not replace professional legal advice. Always consult with qualified legal professionals for important legal matters.
