# Ai-Powered-Resume-Intelligence

The AI-Driven Resume Intelligence System enables users to upload a ZIP file containing multiple PDF resumes. Each resume is processed using Google Gemini LLM via LangChain to extract key candidate details. The extracted information is then organized into a structured format and exported as a downloadable CSV file for easy review and analysis.

Features:
-Bulk resume processing via ZIP file upload
-PDF resume text extraction using PyMuPDF
-AI-powered information extraction with Google Gemini LLM
-Structured output enforcement using LangChain TypedDict
-Automatic CSV generation for recruiter-friendly analysis
-Interactive and clean UI built with Streamlit

Tech Stack
Programming Language: Python
Frontend: Streamlit
LLM Integration: Google Gemini (via LangChain)
PDF Processing: PyMuPDF
Data Handling: Pandas

Extracted Information
The system extracts the following details from each resume:
Candidate Name
Email Address
Phone Number
LinkedIn Profile
GitHub Profile
Professional Summary
Technical Summary
Certifications

