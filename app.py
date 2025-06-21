import streamlit as st
from resume_parser import parse_resume
from job_matcher import match_skills, generate_feedback

st.title("🧠 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    data = parse_resume("temp_resume.pdf")
    st.subheader("🔍 Extracted Information:")
    st.json(data)

    desired_skills = ['Python', 'Machine Learning', 'Deep Learning', 'Docker', 'AWS']
    candidate_skills = data.get('skills', [])

    matched, missing = match_skills(candidate_skills, desired_skills)

    st.subheader("✅ Skill Match:")
    st.write("**Matched Skills:**", matched)
    st.write("**Missing Skills:**", missing)

    feedback = generate_feedback(missing)
    st.subheader("📌 Feedback:")
    for tip in feedback:
        st.write("-", tip)
