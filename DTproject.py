import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os
import PyPDF2

# Load environment variables
load_dotenv()

# Set up API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAlLAYBLWdAFmTMM8_p2WogdSJXd9lbDSE"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text using TTS
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's response using speech-to-text
def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        st.write("Listening for your answer...")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            return user_input
        except sr.UnknownValueError:
            speak_text("Sorry, I couldn't understand that. Could you please repeat?")
            return None
        except sr.RequestError:
            speak_text("Sorry, I am having trouble connecting to the speech recognition service.")
            return None

# Function to fetch response from Gemini AI
def get_gemini_response(input_text, additional_content, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([input_text, additional_content, prompt])
    return response

# Function to extract text from PDF
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ''
        for page in reader.pages:
            pdf_text += page.extract_text() + '\n'
        if pdf_text.strip() == '':
            raise ValueError("No text found in the PDF file.")
        return pdf_text
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app configuration
st.set_page_config(page_title="AI Interview & Resume Analyzer")
st.header("GEN-AI MINIONS")

# User inputs: Job Description and Resume
job_description = st.text_area("Job Description: ", key="job_desc")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])
if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Buttons for features
start_interview_button = st.button("Start Mock Interview")
submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improve My Skills")
submit3 = st.button("Percentage Match")
submit4 = st.button("Suggest Relevant Certifications")

# Prompts for resume analysis
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a career coach with expertise in skill-building and career development. Based on the provided job description and resume, 
suggest actionable skills the candidate should develop or improve to increase their suitability for the job role. 
Include both technical and soft skills.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide the percentage match if the resume matches
the job description. First, the output should come as a percentage, followed by missing keywords, and lastly, your final thoughts.
"""

input_prompt4 = """
You are an AI career advisor with extensive knowledge of professional certifications across various domains. 
Based on the given job description and resume, suggest relevant certifications that can enhance the candidate's profile 
and increase their suitability for the role.
"""

# Feature: Start Mock Interview
if start_interview_button:
    if job_description:
        speak_text("Welcome to the mock interview. I will ask you questions based on the job description.")
        st.write("Starting mock interview...")
        
        input_prompt = """
        You are an interview panelist for a job. Ask relevant questions to the candidate based on the job description provided.
        After the candidate answers, evaluate the response based on industry standards and provide constructive feedback.
        """

        # Generate initial question based on the job description
        first_question_response = get_gemini_response(job_description, "", input_prompt)
        question_text = first_question_response.text.strip()

        # Speak and display the question
        speak_text(question_text)
        st.write(f"Question: {question_text}")

        # Listen to candidate's answer
        user_answer = listen_to_user()

        if user_answer:
            st.write(f"Your answer: {user_answer}")
            # Fetch feedback for the candidate's answer
            feedback_prompt = """
            You are a hiring manager. Based on the candidate's response and the job description provided, 
            evaluate the candidate's answer. Provide feedback on how well the answer matches the job requirements.
            """
            feedback_response = get_gemini_response(user_answer, job_description, feedback_prompt)
            st.subheader("Feedback:")
            st.write(feedback_response.text)
        else:
            st.write("No answer detected. Please try again.")
    else:
        st.write("Please provide the job description to start the mock interview.")

# Feature: Tell Me About the Resume
elif submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(job_description, pdf_content, input_prompt1)
        st.subheader("Resume Evaluation")
        st.write(response.text)
    else:
        st.write("Please upload the resume")

# Feature: How Can I Improve My Skills
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(job_description, pdf_content, input_prompt2)
        st.subheader("Skill Improvement Suggestions")
        st.write(response.text)
    else:
        st.write("Please upload the resume")

# Feature: Percentage Match
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(job_description, pdf_content, input_prompt3)
        st.subheader("Percentage Match")
        st.write(response.text)
    else:
        st.write("Please upload the resume")

# Feature: Suggest Relevant Certifications
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(job_description, pdf_content, input_prompt4)
        st.subheader("Suggested Certifications")
        st.write(response.text)
    else:
        st.write("Please upload the resume")
