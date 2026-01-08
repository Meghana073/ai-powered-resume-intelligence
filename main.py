import streamlit as st
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import pymupdf
from typing import TypedDict, Annotated
import zipfile
import pandas as pd

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("Gem")

st.set_page_config(page_title="AI Resume Intelligence",layout="centered")

st.title("AI-Driven Resume Intelligence System")

st.markdown("""Upload a **ZIP file containing multiple resumes (PDF)**.  
The system extracts key candidate information and exports it as a **CSV file**.""")

uploaded_zip = st.file_uploader("Upload Resume ZIP File",type=["zip"])

# Initialize LLM model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite",temperature=0.2)

# Design Data Format
class DataFormat(TypedDict):
    Candidate_name: Annotated[str, "Extract the full name"]
    Email_address: Annotated[str, "Extract the email address"]
    Phone_number: Annotated[str, "Extract the phone number"]
    Linked_url: Annotated[str, "Extract the LinkedIn URL"]
    Github_url: Annotated[str, "Extract the GitHub URL"]
    Professional_summary: Annotated[str, "Extract professional summary"]
    Technical_summary: Annotated[str, "Extract technical summary"]
    Certifications: Annotated[list[str], "Extract certifications"]

final_model = model.with_structured_output(DataFormat)

# Prompt template
prompt = PromptTemplate(template="""Extract the following information from the resume text below.
                        Resume:{resume}
                        Return output using EXACTLY these keys:
                        Candidate_name
                        Email_address
                        Phone_number
                        Linked_url
                        Github_url
                        Professional_summary
                        Technical_summary
                        Certifications
                        """,
                    input_variables=["resume"])

extract_path = "extracted_resume"

if uploaded_zip is not None:
    st.success("ZIP file uploaded successfully")

    if st.button("Process Resumes"):
        results = []

        with st.spinner("Processing resumes... Please wait"):
            
            # Extract ZIP directly from uploaded file
            with zipfile.ZipFile(uploaded_zip, "r") as zip:
                zip.extractall(extract_path)

            # Process extracted PDFs
            for file in os.listdir(extract_path):
                if file.lower().endswith(".pdf"):
                    pdf_path = os.path.join(extract_path, file)

                    text = ""
                    doc = pymupdf.open(pdf_path)
                    for page in doc:
                        text += page.get_text()
                    doc.close()

                    formatted_prompt = prompt.format(resume=text)
                    response = final_model.invoke(formatted_prompt)

                    response["resume_file"] = file
                    results.append(response)

        st.success("Resumes processed successfully!")

        df = pd.DataFrame(results)
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download CSV",
            data=csv,
            file_name="resume_extracted_data.csv",
            mime="text/csv"
        )

else:
    st.info("Please upload a ZIP file to continue.")




