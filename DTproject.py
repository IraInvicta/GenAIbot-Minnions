from dotenv import load_dotenv
import streamlit as st
import os
import PyPDF2
import google.generativeai as genai

load_dotenv()


os.environ["GOOGLE_API_KEY"] = "apikey"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

st.set_page_config(page_title="GEN-AI MINIONS")
st.header("GEN-AI MINIONS")


def get_gemini_response(input_text, pdf_content, prompt):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")  
        response = model.generate_content([input_text, pdf_content, prompt])
        return response.result  
    except Exception as e:
        return f"Error fetching response from Gemini API: {e}"
    
        return response.messages[-1]['content']  
    except Exception as e:
        st.error(f"Error fetching response from Gemini API: {e}")
        return None

def input_pdf_setup(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ''.join([page.extract_text() for page in reader.pages])
        
        if not pdf_text.strip():
            raise ValueError("No text found in the PDF file.")
        return pdf_text
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None


input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF):", type=["pdf"])

if uploaded_file:
    st.success("PDF Uploaded Successfully!")


submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improve My Skills")
submit3 = st.button("Percentage Match")


input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide the percentage match if the resume matches
the job description. First, the output should come as a percentage, followed by missing keywords, and lastly, your final thoughts.
"""

if submit1 or submit3:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            prompt = input_prompt1 if submit1 else input_prompt3
            response = get_gemini_response(prompt,input_text,pdf_content)
            if response:
                st.subheader("The Response is:")
                st.write(response)  
            else:
                st.error("Failed to fetch the response. Please try again.")
    else:
        st.warning("Please upload the resume before proceeding.")
