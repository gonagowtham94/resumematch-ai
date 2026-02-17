import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------
# Text Cleaning
# --------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


# --------------------------
# Generic Words To Ignore
# --------------------------

GENERIC_WORDS = {
    "project", "projects", "development", "system", "application",
    "experience", "work", "working", "team", "skills",
    "knowledge", "using", "based", "design", "role",
    "candidate", "requirement", "analysis"
}


# --------------------------
# Match Score Calculation
# --------------------------

def calculate_match_score(resume_text, job_text):

    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=7000
    )

    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    raw_score = similarity[0][0]

    # ATS calibrated score
    calibrated_score = (raw_score * 3.2 * 100) + 15

    if calibrated_score > 100:
        calibrated_score = 100

    return round(calibrated_score, 2)


# --------------------------
# Extract Matching Skills (Dynamic)
# --------------------------

def extract_common_keywords(resume_text, job_text):

    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
    feature_names = vectorizer.get_feature_names_out()

    resume_vector = tfidf_matrix.toarray()[0]
    job_vector = tfidf_matrix.toarray()[1]

    matched_keywords = []

    for i in range(len(feature_names)):
        if resume_vector[i] > 0 and job_vector[i] > 0:

            word = feature_names[i]

            # Filtering logic
            if (
                word not in GENERIC_WORDS
                and len(word) > 2
            ):
                matched_keywords.append(word)

    return matched_keywords[:15]   # limit to top 15
