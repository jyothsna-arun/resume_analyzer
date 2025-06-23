import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import re

# --- Page Configuration ---
st.set_page_config(page_title="AI Resume Analyzer", page_icon=":rainbow:", layout="centered")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #fcefee, #ccf2f4);
            color: #333333;
        }
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #FF4B91;
            text-align: center;
            padding: 10px;
        }
        .section-header {
            font-size: 26px;
            color: #FF4B91;
            margin-top: 30px;
            border-bottom: 2px dashed #FF4B91;
            padding-bottom: 5px;
        }
        .stFileUploader, .stTextArea {
            background-color: #fff !important;
            border: 2px solid #FF4B91 !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }
        textarea {
            color: #333333 !important;
            background-color: #ffffff !important;
        }
        .stMetric {
            background-color: #ffffff30 !important;
            border-radius: 12px;
            padding: 8px;
        }
        .stAlert {
            background-color: #FFEBF0 !important;
            color: #FF004D !important;
            border-radius: 8px;
        }
        .stButton > button {
            background-color: #FF4B91;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #e8437c;
            color: white;
        }
        .skill-badge {
            display: inline-block;
            background-color: #E0F7FA;
            color: #00796B;
            padding: 6px 12px;
            margin: 5px 5px 5px 0;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# --- Main Title ---
st.markdown('<div class="title">🌈 AI Resume Analyzer</div>', unsafe_allow_html=True)

# --- File Uploader ---
st.markdown('<h3 class="section-header">📤 Upload your Resume (PDF or DOCX)</h3>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=['pdf', 'docx'])

# --- Job Description Text Area ---
st.markdown('<h3 class="section-header">📝 Paste Job Description Here</h3>', unsafe_allow_html=True)

st.markdown("""
    <div style="font-size:16px; color:#556B2F; font-weight:bold; margin-bottom:5px;">
        Once done typing do ctrl+enter for next process !
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    div[data-baseweb="textarea"] textarea {
        border: 1px solid #ccc !important;
        outline: none !important;
        box-shadow: none !important;
        border-radius: 6px !important;
        padding: 8px;
        caret-color: black !important;
        color: black !important;
        font-size: 16px !important;
        background-color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

job_description = st.text_area("", height=200)

# --- Functions ---
def read_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text

def read_docx(file):
    doc = Document(file)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

def extract_text(file):
    if file.name.endswith('.pdf'):
        return read_pdf(file)
    elif file.name.endswith('.docx'):
        return read_docx(file)
    else:
        return None

def extract_skills(text):
    skills = ['Python', 'C', 'C++', 'HTML', 'CSS', 'Java', 'JavaScript', 'SQL',
              'Machine Learning', 'Deep Learning', 'Data Analysis', 'Pandas', 'NumPy', 'TensorFlow']
    extracted = [skill for skill in skills if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]
    return list(set(extracted))

def extract_jd_skills(jd_text):
    return extract_skills(jd_text)

def calculate_match(resume_skills, jd_text):
    jd_skills = extract_skills(jd_text)
    match_count = len(set(resume_skills) & set(jd_skills))
    return int((match_count / len(jd_skills)) * 100) if jd_skills else 0

# --- Skill Extraction Section ---
st.markdown('<h3 class="section-header">🔍 Skill Extraction</h3>', unsafe_allow_html=True)

if uploaded_file is not None:
    resume_text = extract_text(uploaded_file)
    extracted_resume_skills = extract_skills(resume_text)

    st.markdown("📄 **Extracted Resume Skills**")

    if extracted_resume_skills:
        badges = ' '.join([f"<span class='skill-badge'>{skill}</span>" for skill in extracted_resume_skills])
        st.markdown(badges, unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div style="background-color:#FFEBEE; padding:12px 16px; border-radius:8px; 
                        color:#B00020; font-weight:600; font-size:18px;">
                ⚠️ No skills found in the uploaded resume.
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    extracted_resume_skills = []

# --- Resume Match Score Section ---
st.markdown('<h3 class="section-header">📊 Resume Match Score</h3>', unsafe_allow_html=True)

if uploaded_file is not None and job_description.strip() != '':
    jd_skills = extract_jd_skills(job_description)
    match_score = calculate_match(extracted_resume_skills, job_description)

    st.markdown(
        f"""
        <div style="color:#00008B; font-weight:bold; font-size:22px;">
            Match Score (%): {match_score} %
        </div>
        """,
        unsafe_allow_html=True
    )
    st.progress(match_score / 100)

    st.markdown("🔧 **Skills from Job Description**")
    if jd_skills:
        jd_badges = ' '.join([f"<span class='skill-badge'>{skill}</span>" for skill in jd_skills])
        st.markdown(jd_badges, unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div style="background-color:#E6F0FF; padding:12px 16px; border-radius:8px; 
                        color:#00008B; font-weight:600; font-size:18px;">
                ℹ️ No recognizable skills found in the job description.
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- Matched Skills ---
    matched = list(set(extracted_resume_skills) & set(jd_skills))
    if matched:
        st.markdown("✅ **Matched Skills**:")
        matched_badges = ' '.join([f"<span class='skill-badge'>{skill}</span>" for skill in matched])
        st.markdown(matched_badges, unsafe_allow_html=True)

    # --- Missing Skills ---
    missing = list(set(jd_skills) - set(extracted_resume_skills))
    if missing:
        st.markdown("❌ **Missing Skills**:")
        missing_badges = ' '.join([
            f"<span class='skill-badge' style='background-color:#FFEBEE;color:#D32F2F;'>{skill}</span>"
            for skill in missing
        ])
        st.markdown(missing_badges, unsafe_allow_html=True)

else:
    st.markdown(
        "<span style='color: black; font-size:16px;'>Please upload a resume and paste a job description to see the match score.</span>",
        unsafe_allow_html=True
    )

# --- Footer ---
st.markdown("<br><hr><center>Created By Jyothsna A</center>", unsafe_allow_html=True)
