# apps/posts/sources/category_detector.py

import re


# ============================================================
# CATEGORY KEYWORDS
# ============================================================

CATEGORY_KEYWORDS = {

    "Admit Card": [
        "admit card",
        "admit-card",
        "e-admit card",
        "hall ticket",
        "call letter",
        "download admit",
        "admission certificate",
    ],

    "Answer Key": [
        "answer key",
        "answer-key",
        "answer keys",
        "provisional answer key",
        "final answer key",
        "response sheet",
        "response-sheet",
        "candidates response sheet",
        "candidate response sheet",
        "response sheets",
        "objection tracker",
    ],

    "Result": [
        "result",
        "final result",
        "written result",
        "exam result",
        "result write-up",
        "result writeup",
        "merit list",
        "selection list",
        "shortlisted candidates",
        "qualified candidates",
        "selected candidates",
        "marks of candidates",
        "score card",
        "scorecard",
    ],

    "Syllabus": [
        "syllabus",
        "exam syllabus",
        "detailed syllabus",
        "course syllabus",
        "exam pattern",
    ],

    "Admission": [
        "admission",
        "entrance exam",
        "entrance test",
        "counselling",
        "counseling",
        "university admission",
        "college admission",
        "information bulletin",
    ],

    "Documents": [
        "calling options",
        "calling option",
        "option preference",
        "options preferences",
        "option/preferences",
        "allocation of zones",
        "allocation of zone",
        "allocation of formations",
        "allocation",
        "document verification",
        "certificate verification",
        "verification notice",
        "verification",
        "corrigendum",
        "addendum",
        "important notice",
        "notice",
        "instructions",
        "instruction",
        "schedule of examination",
        "schedule of exam",
        "extension notice",
        "date extension",
        "revised schedule",
        "withdrawal notice",
        "modification notice",
        "clarification",
    ],

    "Latest Jobs": [
        "recruitment",
        "recruitment notification",
        "vacancy",
        "vacancies",
        "online application",
        "apply online",
        "application form",
        "online form",
        "job notification",
        "job",
        "posts",
        "post",
        "engagement",
        "hiring",
        "registration",
        "applications are invited",
        "application invited",
    ],
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Converts text into a clean lowercase format
    so keyword matching becomes reliable.
    """

    if not text:
        return ""

    text = str(text).lower()

    # Replace special characters with spaces
    text = re.sub(r"[^a-z0-9\s\-/]", " ", text)

    # Convert multiple spaces into one
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# CATEGORY DETECTOR
# ============================================================

def detect_category(title, description=""):
    """
    Automatically detects the correct SarkariJobs category.

    Priority:
    1. Admit Card
    2. Answer Key
    3. Result
    4. Admission
    5. Syllabus
    6. Documents
    7. Latest Jobs
    """

    title_text = normalize_text(title)
    description_text = normalize_text(description)

    full_text = f"{title_text} {description_text}".strip()

    if not full_text:
        return "Latest Jobs"


    # --------------------------------------------------------
    # 1. ADMIT CARD
    # --------------------------------------------------------

    for keyword in CATEGORY_KEYWORDS["Admit Card"]:
        if normalize_text(keyword) in full_text:
            return "Admit Card"


    # --------------------------------------------------------
    # 2. ANSWER KEY
    # --------------------------------------------------------

    for keyword in CATEGORY_KEYWORDS["Answer Key"]:
        if normalize_text(keyword) in full_text:
            return "Answer Key"


    # --------------------------------------------------------
    # 3. RESULT
    # --------------------------------------------------------

    for keyword in CATEGORY_KEYWORDS["Result"]:
        if normalize_text(keyword) in full_text:
            return "Result"


    # --------------------------------------------------------
    # 4. ADMISSION
    # --------------------------------------------------------

    for keyword in CATEGORY_KEYWORDS["Admission"]:
        if normalize_text(keyword) in full_text:
            return "Admission"


    # --------------------------------------------------------
    # 5. SYLLABUS
    # --------------------------------------------------------

    for keyword in CATEGORY_KEYWORDS["Syllabus"]:
        if normalize_text(keyword) in full_text:
            return "Syllabus"


    # --------------------------------------------------------
    # 6. DOCUMENTS / IMPORTANT NOTICES
    # --------------------------------------------------------

    for keyword in CATEGORY_KEYWORDS["Documents"]:
        if normalize_text(keyword) in full_text:
            return "Documents"


    # --------------------------------------------------------
    # 7. LATEST JOBS
    # --------------------------------------------------------

    for keyword in CATEGORY_KEYWORDS["Latest Jobs"]:
        if normalize_text(keyword) in full_text:
            return "Latest Jobs"


    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    return "Latest Jobs"