import re

def extract_keywords(text):
    return set(re.findall(r'\b\w+\b', text.lower()))


def analyze_text(resume_text, job_desc):
    resume_words = extract_keywords(resume_text)
    job_words = extract_keywords(job_desc)

    all_skills = ["python", "html", "css", "javascript", "sql", "react", "node", "mongodb"]

    skills_found = []
    missing_skills = []

    for skill in all_skills:
        if skill in resume_text.lower():
            skills_found.append(skill.capitalize())
        else:
            missing_skills.append(skill.capitalize())

    return skills_found, missing_skills[:5], 0


def calculate_ats_score(resume_text, job_desc, skills_found, missing_skills):

    resume_words = extract_keywords(resume_text)
    job_words = extract_keywords(job_desc)

    total_skills = len(skills_found) + len(missing_skills)
    skills_score = (len(skills_found) / total_skills) * 100 if total_skills else 0

    matched_keywords = resume_words.intersection(job_words)
    keyword_score = (len(matched_keywords) / len(job_words)) * 100 if job_words else 0

    experience_keywords = ["years", "experience", "developed", "built"]
    exp_score = sum(1 for word in experience_keywords if word in resume_text.lower()) * 20
    exp_score = min(exp_score, 100)

    education_keywords = ["bachelor", "master", "degree", "b.tech", "bsc", "msc"]
    edu_score = sum(1 for word in education_keywords if word in resume_text.lower()) * 25
    edu_score = min(edu_score, 100)

    formatting_score = 80

    ats_score = (
        0.40 * skills_score +
        0.25 * keyword_score +
        0.15 * exp_score +
        0.10 * edu_score +
        0.10 * formatting_score
    )

    return round(ats_score, 2)