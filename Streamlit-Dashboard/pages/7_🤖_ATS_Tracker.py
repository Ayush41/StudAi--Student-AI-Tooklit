from dotenv import load_dotenv
import streamlit as st
from utils.auth import check_auth, show_login_page

if not check_auth():
    show_login_page()
    st.stop()  # Prevent access to the feature
    
# Rest of your feature page code...


load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")



   
















# import streamlit as st
# import google.generativeai as genai
# import os
# import PyPDF2 as pdf
# from dotenv import load_dotenv
# import json

# load_dotenv() ## load all our environment variables

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_repsonse(input):
#     model=genai.GenerativeModel('gemini-1.5-flash')
#     response=model.generate_content(input)
#     return response.text

# def input_pdf_text(uploaded_file):
#     reader=pdf.PdfReader(uploaded_file)
#     text=""
#     for page in range(len(reader.pages)):
#         page=reader.pages[page]
#         text+=str(page.extract_text())
#     return text

# #Prompt Template

# input_prompt="""
# Hey Act Like a skilled or very experience ATS(Application Tracking System)
# with a deep understanding of tech field,software engineering,data science ,data analyst
# and big data engineer. Your task is to evaluate the resume based on the given job description.
# You must consider the job market is very competitive and you should provide 
# best assistance for improving thr resumes. Assign the percentage Matching based 
# on Jd and
# the missing keywords with high accuracy
# resume:{text}
# description:{jd}

# I want the response in one single string having the structure
# {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
# """
# # {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}

# ## streamlit app
# st.title("Smart ATS")
# st.text("Improve Your Resume ATS")
# jd=st.text_area("Paste the Job Description")
# uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

# submit = st.button("Submit")

# if submit:
#     if uploaded_file is not None:
#         text=input_pdf_text(uploaded_file)
#         response=get_gemini_repsonse(input_prompt)
#         st.subheader(response)


# import streamlit as st
# import google.generativeai as genai
# import PyPDF2 as pdf
# from dotenv import load_dotenv
# from streamlit_lottie import st_lottie 
# import json
# import os

# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel('gemini-pro')

# def main():
#     st.write("<h1><center>Applicant tracking systems</center></h1>", unsafe_allow_html=True)
#     st.text("👉🏻                  Personal ATS for Job-Seekers & Recruiters                   👈")
#     with open('src/ATS.json') as anim_source:
#         animation = json.load(anim_source)
#     st_lottie(animation, 1, True, True, "high", 200, -200)
    
#     if 'is_logged' not in st.session_state:
#         st.session_state['is_logged'] = False

#     if st.session_state['is_logged']:
#         st.text_input("Job Role")
#         desc = st.text_area("Paste the Job Description")
#         uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Pls Upload PDF file Only")
#         submit = st.button("Submit")

#         if submit:
#             if uploaded_file is not None:
#                 reader = pdf.PdfReader(uploaded_file)
#                 text = ""
#                 for page_number in range(len(reader.pages)):
#                     page = reader.pages[page_number] 
#                     text += str(page.extract_text())

#                 input_prompt = f'''
#                 You're a skilled ATS (Applicant Tracking System) Scanner with a deep understanding of tech roles, software development, 
#                 tech consulting, and understand the ATS role in-depth. Your task is to evaluate the resume against the given description. 
#                 You must consider that the job market is crowded with applications and you should only pick the best talent. 
#                 Thus, assign the percentage & MissingKeywords with honesty & accuracy
#                 resume: {text}
#                 description: {desc}
#                 I want a output in one single string having the structure: {{"PercentageMatch": "%", "MissingKeywordsintheResume": [], "ProfileSummary": ""}}.
#                 '''

#                 with st.spinner("Evaluating Profile..."):
#                     response = model.generate_content(input_prompt)
#                 response_data = json.loads(response.text)
#                 # st.write(response.text)

#                 st.subheader("ATS Scanner Dashboard")
#                 st.subheader("Candidate Evaluation Results")
#                 st.text(f"Percentage Match: {response_data['PercentageMatch']}")
#                 st.subheader("Missing Keywords in the Resume")
#                 for keyword in response_data['MissingKeywordsintheResume']:
#                     st.text(keyword)
#                 st.subheader("Profile Summary")
#                 st.markdown(response_data['ProfileSummary'])
#         if st.button("Logout"):
#             st.session_state['is_logged'] = False
#             del st.session_state['user']
#             st.rerun()
#     else:
#         st.markdown("<h3 style='text-align: center; color: red;'>You are not Logged In</h3>", unsafe_allow_html=True)
