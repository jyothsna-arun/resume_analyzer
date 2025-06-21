import os
from pyresparser import ResumeParser

def match_skills(candidate_skills, job_skills):
    matched = list(set(candidate_skills) & set(job_skills))
    missing = list(set(job_skills) - set(candidate_skills))
    return matched, missing

def generate_feedback(missing_skills):
    return [f"Consider learning or improving: {skill}" for skill in missing_skills]

def parse_resume(file_path):
    try:
        data = ResumeParser(file_path).get_extracted_data()
        return data.get('skills', [])
    except Exception as e:
        print(f"Failed to parse {file_path}: {e}")
        return []

def analyze_resume(file_path, desired_skills):
    print("="*60)
    print(f"Analyzing: {os.path.basename(file_path)}")
    candidate_skills = parse_resume(file_path)

    if not candidate_skills:
        print("⚠️ No skills extracted.\n")
        return

    print("Extracted Skills:", candidate_skills)

    matched, missing = match_skills(candidate_skills, desired_skills)

    print("Matched Skills:", matched)
    print("Missing Skills:", missing)

    feedback = generate_feedback(missing)
    print("\nFeedback:")
    for item in feedback:
        print("-", item)
    print("="*60 + "\n")

# ---------- CONFIGURATION ----------
desired_skills = ['Python', 'Machine Learning', 'Deep Learning', 'Docker', 'AWS']
resume_folder = "D:/PROJECT/resumeanalyser/SAMPLES"

# ---------- EXECUTE ----------
if __name__ == "__main__":
    for file in os.listdir(resume_folder):
        if file.endswith(".pdf"):
            full_path = os.path.join(resume_folder, file)
            analyze_resume(full_path, desired_skills)
