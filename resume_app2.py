import json
import streamlit as st
import re
import pandas as pd


course_recommendations = {
    "python": [
        {"title": "Python for Everybody", "platform": "Coursera", "link": "https://www.coursera.org/specializations/python"},
        {"title": "Learn Python - Full Course", "platform": "YouTube", "link": "https://youtu.be/rfscVS0vtbw"}
    ],
    "machine learning": [
        {"title": "Machine Learning by Andrew Ng", "platform": "Coursera", "link": "https://www.coursera.org/learn/machine-learning"},
        {"title": "Intro to ML", "platform": "Google", "link": "https://developers.google.com/machine-learning/crash-course"}
    ],
    "nlp": [
        {"title": "Natural Language Processing Specialization", "platform": "Coursera", "link": "https://www.coursera.org/specializations/natural-language-processing"},
        {"title": "Intro to NLP", "platform": "YouTube", "link": "https://youtu.be/8rXD5-xhemo"}
    ],
    "data analysis": [
        {"title": "Data Analyst Career Path", "platform": "DataCamp", "link": "https://www.datacamp.com/career-tracks/data-analyst"},
        {"title": "Data Analysis with Python", "platform": "FreeCodeCamp", "link": "https://youtu.be/r-uOLxNrNk8"}
    ]
    # Add more skills and courses as needed
}


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


def get_course_recommendations(missing_skills, course_db):
    recommendations = []
    for skill in missing_skills:
        skill_lower = skill.lower()
        if skill_lower in course_db:
            for course in course_db[skill_lower]:
                recommendations.append({
                    "Skill": skill,
                    "Course Title": course["title"],
                    "Platform": course["platform"],
                    "Link": course["link"]
                })
    return recommendations

missing_skills = ["Python", "Machine Learning", "Data Analysis"]  # example


# Get recommendations
recommendations = get_course_recommendations(missing_skills, course_recommendations)

# Show in Streamlit
if recommendations:
    st.subheader("📚 Recommended Courses to Improve Your Skills")
    df = pd.DataFrame(recommendations)
    for i in range(len(df)):
        st.markdown(f"**🔧 Skill:** {df.iloc[i]['Skill']}")
        st.markdown(f"- 📘 [{df.iloc[i]['Course Title']}]({df.iloc[i]['Link']}) – *{df.iloc[i]['Platform']}*")
        st.markdown("---")
else:
    st.success("🎉 Your skills are well aligned with the job requirements!")