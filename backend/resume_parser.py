import fitz  # PyMuPDF
import docx2txt
import os
import re


# -----------------------------
# Text Cleaner (Common)
# -----------------------------

def clean_text(text):

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text


# -----------------------------
# PDF Extraction (HIGH QUALITY)
# -----------------------------

def extract_text_from_pdf(file_path):

    text = ""

    pdf_document = fitz.open(file_path)

    for page in pdf_document:
        text += page.get_text()

    pdf_document.close()

    text = clean_text(text)

    return text


# -----------------------------
# DOCX Extraction
# -----------------------------

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)


# -----------------------------
# Main Resume Extractor
# -----------------------------

def extract_resume_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    else:
        return "Unsupported file format"
