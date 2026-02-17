from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

from resume_parser import extract_resume_text
from matcher import calculate_match_score, extract_common_keywords


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------------------
# Frontend Page Routes
# ---------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/insights")
def insights():
    return render_template("insights.html")


@app.route("/about")
def about():
    return render_template("about.html")


# ---------------------------
# Resume Analysis API
# ---------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return jsonify({"status": "error", "message": "No resume uploaded"})

    resume_file = request.files["resume"]
    job_description = request.form.get("job_description")

    if not job_description:
        return jsonify({"status": "error", "message": "Job description missing"})

    # Save uploaded resume
    file_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
    resume_file.save(file_path)

    # Extract resume text
    resume_text = extract_resume_text(file_path)

    # Calculate match score
    score = calculate_match_score(resume_text, job_description)

    # Extract matched skills/keywords
    matched_keywords = extract_common_keywords(resume_text, job_description)

    return jsonify({
        "status": "success",
        "match_percentage": score,
        "common_keywords": matched_keywords
    })


# ---------------------------
# Run Server (Render Compatible)
# ---------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
