from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# 🔑 OpenAI client (new SDK तरीका)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Home route
@app.route("/")
def home():
    return "Server is running with AI ✅"


# ✅ Extract text from PDF
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


# 🤖 AI Suggestions Function (UPDATED)
def ai_suggestions(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Analyze this resume and give:
                    1. Key strengths
                    2. Missing skills for software developer
                    3. Suggestions to improve

                    Resume:
                    {text}
                    """
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI Error:", e)  # useful for debugging in Render logs
        return "AI suggestions not available"


# 🧠 Skill + Matching Logic
def analyze_text(text, job_desc=""):
    text = text.lower()

    all_skills = ["python", "html", "css", "javascript", "sql", "react", "node", "mongodb"]

    skills_found = []
    missing_skills = []

    for skill in all_skills:
        if skill in text:
            skills_found.append(skill.capitalize())
        else:
            missing_skills.append(skill.capitalize())

    # 🎯 Job Match Score
    match_score = 0
    if job_desc:
        job_desc = job_desc.lower()
        matched = [skill for skill in all_skills if skill in job_desc and skill in text]
        match_score = int((len(matched) / len(all_skills)) * 100)

    return skills_found, missing_skills[:5], match_score


# 🚀 Main API
@app.route("/analyze", methods=["POST"])
def analyze_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    job_desc = request.form.get("job_desc", "")

    if file.filename == "":
        return jsonify({"error": "Empty file"}), 400

    # Extract text
    text = extract_text(file)

    # Skill analysis
    skills_found, missing_skills, match_score = analyze_text(text, job_desc)

    # AI Suggestions
    suggestion = ai_suggestions(text)

    return jsonify({
        "skills_found": skills_found,
        "missing_skills": missing_skills,
        "match_score": match_score,
        "suggestion": suggestion
    })


# ▶️ Run server
if __name__ == "__main__":
    app.run(debug=True)