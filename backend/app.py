from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Import our modules
from resume_parser import extract_resume_text
from matcher import calculate_match_score, extract_common_keywords

# ---------------------------
# Flask App Setup
# ---------------------------

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------------------
# Home Route (Test)
# ---------------------------

@app.route("/")
def home():
    return "ResumeMatch AI Backend Running Successfully 🚀"


# ---------------------------
# Resume Analysis API
# ---------------------------

@app.route("/analyze", methods=["POST"])
def analyze_resume():

    # Check resume file
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    resume_file = request.files["resume"]

    # Check job description
    job_description = request.form.get("job_description")

    if resume_file.filename == "":
        return jsonify({"error": "No resume file selected"}), 400

    if not job_description:
        return jsonify({"error": "Job description is missing"}), 400

    # Save uploaded resume
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
    resume_file.save(file_path)

    # ---------------------------
    # Resume Text Extraction
    # ---------------------------

    resume_text = extract_resume_text(file_path)
    print("========== RESUME TEXT PREVIEW ==========")
    print(resume_text[:800])
    print("========================================")


    if resume_text == "Unsupported file format":
        return jsonify({"error": "Unsupported resume format"}), 400

    # ---------------------------
    # NLP Matching Engine
    # ---------------------------

    match_percentage = calculate_match_score(resume_text, job_description)

    common_keywords = extract_common_keywords(resume_text, job_description)

    # ---------------------------
    # Send Response
    # ---------------------------

    return jsonify({
        "status": "success",
        "match_percentage": match_percentage,
        "common_keywords": common_keywords,
        "message": "Resume analyzed successfully"
    })


# ---------------------------
# Run Server
# ---------------------------

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
