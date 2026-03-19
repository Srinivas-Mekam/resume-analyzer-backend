from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.pdf_parser import extract_text
from utils.ats import analyze_text, calculate_ats_score
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Resume Analyzer API Running ✅"


@app.route("/analyze", methods=["POST"])
def analyze_resume():
    try:
        file = request.files.get("resume")
        job_desc = request.form.get("job_desc", "")

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Extract text
        text = extract_text(file)

        # ATS analysis
        skills_found, missing_skills, _ = analyze_text(text, job_desc)
        ats_score = calculate_ats_score(text, job_desc, skills_found, missing_skills)

        return jsonify({
            "skills_found": skills_found,
            "missing_skills": missing_skills,
            "match_score": ats_score
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)