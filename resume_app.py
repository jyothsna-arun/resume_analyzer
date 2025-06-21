import streamlit as st
import re

st.title("📝 AI Resume Analyzer")

# Resume Upload
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf", "docx"])

# Job Description Input
jd_text = st.text_area("Paste Job Description Here", height=200)

# Sample skill list (you can expand this)
known_skills = [
    "python", "java", "c++", "sql", "machine learning", "deep learning",
    "nlp", "data analysis", "data science", "tensorflow", "pandas",
    "numpy", "flask", "django", "excel", "communication", "teamwork"
]

resume_skills = ['python', 'sql', 'teamwork', 'django']


def extract_skills_from_jd(jd_text, skill_set):
    jd_text = jd_text.lower()
    extracted = set()
    for skill in skill_set:
        # match exact word using regex
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, jd_text):
            extracted.add(skill)
    return list(extracted)

jd_skills = extract_skills_from_jd(jd_text, known_skills)

matched_skills = list(set(resume_skills) & set(jd_skills))
missing_skills = list(set(jd_skills) - set(resume_skills))

if jd_skills:
    match_percent = round((len(matched_skills) / len(jd_skills)) * 100, 2)
else:
    match_percent = 0.0

st.subheader("📊 Skill Matching Results")

st.markdown(f"**Matched Skills ({len(matched_skills)}):** {', '.join(matched_skills)}")
st.markdown(f"**Missing Skills ({len(missing_skills)}):** {', '.join(missing_skills)}")
st.markdown(f"**Match %:** `{match_percent}%`")


