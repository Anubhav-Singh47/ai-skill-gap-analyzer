import re
from html import escape
from io import BytesIO

import pandas as pd
import requests
import streamlit as st
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

# ============================================================
# CONFIG
# ============================================================

BACKEND_URL = "https://ai-skill-gap-analyzer-tn48.onrender.com"

st.set_page_config(
    page_title="AI Skill-Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f7f9fc;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #667085;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .card {
        padding: 24px;
        border-radius: 18px;
        background: white;
        border: 1px solid #e6eaf0;
        box-shadow: 0 5px 18px rgba(0,0,0,0.05);
        margin-bottom: 18px;
    }

    .metric-card {
        padding: 22px;
        border-radius: 16px;
        background: white;
        border: 1px solid #e6eaf0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        min-height: 110px;
    }

    .metric-number {
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .metric-label {
        color: #667085;
        font-size: 14px;
    }

    .success-box {
        padding: 14px 18px;
        border-radius: 12px;
        background: #ecfdf3;
        border: 1px solid #abefc6;
        color: #067647;
        margin-bottom: 15px;
    }

    .warning-box {
        padding: 14px 18px;
        border-radius: 12px;
        background: #fffaeb;
        border: 1px solid #fedf89;
        color: #b54708;
        margin-bottom: 15px;
    }

    .skill-tag {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border-radius: 20px;
        background: #eef4ff;
        color: #344054;
        font-size: 13px;
        border: 1px solid #d1e0ff;
    }

    .missing-tag {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border-radius: 20px;
        background: #fff4ed;
        color: #b42318;
        font-size: 13px;
        border: 1px solid #fecdca;
    }

    .recommendation-card {
        padding: 18px;
        border-radius: 14px;
        background: white;
        border: 1px solid #e6eaf0;
        margin-bottom: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .roadmap-card {
        padding: 18px;
        border-radius: 14px;
        background: white;
        border-left: 5px solid #667085;
        margin-bottom: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .section-title {
        font-size: 28px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "resume_text": "",
    "resume_result": None,
    "skill_result": None,
    "roadmap_result": None,
    "job_match_result": None,
    "ai_recommendation_result": None
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# SKILLS
# ============================================================

ALL_SKILLS = [
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Statistics",
    "Pandas",
    "NumPy",
    "Machine Learning",
    "Scikit-learn",
    "Java",
    "Data Structures",
    "Algorithms",
    "Git",
    "OOP",
    "ETL",
    "Apache Spark",
    "Cloud",
    "HTML",
    "CSS",
    "JavaScript",
    "React"
]

DEFAULT_SKILLS = [
    "Python",
    "Machine Learning",
    "Java",
    "Data Structures",
    "Algorithms",
    "Git",
    "OOP",
    "HTML",
    "CSS",
    "JavaScript",
    "React"
]


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(uploaded_file):

    try:

        reader = PdfReader(uploaded_file)

        pages_text = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages_text.append(text)

        return "\n".join(pages_text).strip()

    except Exception as e:

        st.error(f"Could not read PDF: {e}")

        return ""


# ============================================================
# SKILL DETECTION
# ============================================================

def detect_skills(text):

    if not text:
        return []

    text_lower = text.lower()

    skill_aliases = {

        "Python": [
            "python"
        ],

        "SQL": [
            "sql",
            "mysql",
            "postgresql",
            "database"
        ],

        "Excel": [
            "excel",
            "microsoft excel"
        ],

        "Power BI": [
            "power bi",
            "powerbi"
        ],

        "Statistics": [
            "statistics",
            "statistical"
        ],

        "Pandas": [
            "pandas"
        ],

        "NumPy": [
            "numpy",
            "num py"
        ],

        "Machine Learning": [
            "machine learning",
            "machine-learning"
        ],

        "Scikit-learn": [
            "scikit-learn",
            "scikit learn",
            "sklearn"
        ],

        "JavaScript": [
            "javascript",
            "java script"
        ],

        "Java": [
            "java"
        ],

        "Data Structures": [
            "data structures",
            "data structure",
            "dsa"
        ],

        "Algorithms": [
            "algorithms",
            "algorithm"
        ],

        "Git": [
            "git",
            "github",
            "gitlab"
        ],

        "OOP": [
            "oop",
            "object oriented",
            "object-oriented"
        ],

        "ETL": [
            "etl"
        ],

        "Apache Spark": [
            "apache spark"
        ],

        "Cloud": [
            "cloud",
            "aws",
            "azure",
            "gcp"
        ],

        "HTML": [
            "html"
        ],

        "CSS": [
            "css"
        ],

        "React": [
            "react",
            "reactjs",
            "react.js"
        ]
    }

    detected = []

    for skill, aliases in skill_aliases.items():

        found = False

        for alias in aliases:

            pattern = (
                r"(?<![a-zA-Z0-9])"
                + re.escape(alias.lower())
                + r"(?![a-zA-Z0-9])"
            )

            if re.search(pattern, text_lower):

                found = True
                break

        if found:

            detected.append(skill)

    return detected


# ============================================================
# JOB DESCRIPTION MATCHER
# ============================================================

def calculate_job_match(resume_text, job_description):

    resume_skills = detect_skills(resume_text)

    job_skills = detect_skills(job_description)

    matched_skills = []

    missing_skills = []

    for skill in job_skills:

        if skill in resume_skills:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    if len(job_skills) > 0:

        match_percentage = round(
            (len(matched_skills) / len(job_skills)) * 100
        )

    else:

        match_percentage = 0

    if match_percentage >= 80:

        match_level = "Excellent Match"

    elif match_percentage >= 60:

        match_level = "Good Match"

    elif match_percentage >= 40:

        match_level = "Moderate Match"

    else:

        match_level = "Low Match"

    return {

        "match_percentage": match_percentage,

        "match_level": match_level,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "job_skills": job_skills
    }


# ============================================================
# BACKEND STATUS
# ============================================================

backend_connected = False

try:

    response = requests.get(
        BACKEND_URL,
        timeout=3
    )

    if response.status_code == 200:

        backend_connected = True

except Exception:

    backend_connected = False


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎯 AI Skill-Gap Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered Resume Analysis • Skill Gap Detection • Career Roadmap'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# BACKEND STATUS
# ============================================================

if backend_connected:

    st.markdown(
        """
        <div class="success-box">
        🟢 <b>Backend Connected Successfully</b>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="warning-box">
        🟡 <b>Backend is not connected.</b>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD HEADER
# ============================================================

st.markdown(
    "## 🚀 AI Career Intelligence Dashboard"
)

st.caption(
    "Resume Analysis • Skill Gap Detection • Personalized Career Roadmap"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Profile Settings")

    student_name = st.text_input(
        "Your Name",
        placeholder="Enter your name"
    )

    course = st.text_input(
        "Course",
        placeholder="Example: B.Tech CSE"
    )

    target_role = st.selectbox(
        "🎯 Target Role",
        [
            "Data Analyst",
            "Data Scientist",
            "Software Developer",
            "Data Engineer",
            "Web Developer"
        ]
    )

    st.markdown("---")

    st.markdown("### 🛠️ Current Skills")

    current_skills = st.multiselect(
        "Select your skills",
        ALL_SKILLS,
        default=DEFAULT_SKILLS
    )


# ============================================================
# TOP DASHBOARD CARDS
# ============================================================

# FIX 1:
# Always calculate the detected skill count
# directly from the stored skill list.

if st.session_state.resume_result:

    detected_skills_count = len(
        st.session_state.resume_result.get(
            "skills",
            []
        )
    )

else:

    detected_skills_count = 0


if st.session_state.skill_result:

    top_skill_score = st.session_state.skill_result.get(
        "score",
        0
    )

else:

    top_skill_score = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-number">
        {"Ready" if st.session_state.resume_result else "Pending"}
        </div>

        <div class="metric-label">
        📄 Resume Status
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-number">
        {detected_skills_count}
        </div>

        <div class="metric-label">
        🧠 Skills Detected
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-number">
        {escape(target_role)}
        </div>

        <div class="metric-label">
        🎯 Target Role
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-number">
        {top_skill_score}%
        </div>

        <div class="metric-label">
        📈 Skill Match
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RESUME ANALYSIS
# ============================================================

st.markdown(
    "## 📄 Resume Analysis"
)

uploaded_file = st.file_uploader(
    "Upload your Resume PDF",
    type=["pdf"]
)


if uploaded_file:

    st.info(
        f"📄 {uploaded_file.name}  •  "
        f"{round(uploaded_file.size / 1024, 1)} KB"
    )


if st.button(
    "🚀 Analyze My Resume",
    use_container_width=True
):

    if uploaded_file is None:

        st.warning(
            "Please upload your resume PDF first."
        )

    else:

        with st.spinner(
            "Analyzing your resume..."
        ):

            resume_text = extract_pdf_text(
                uploaded_file
            )

            if resume_text:

                detected = detect_skills(
                    resume_text
                )

                # FIX:
                # Store total_skills as well as skills.

                st.session_state.resume_text = resume_text

                st.session_state.resume_result = {

                    "skills": detected,

                    "total_skills": len(detected),

                    "text": resume_text
                }

                st.session_state.job_match_result = None

                st.success(
                    f"Resume analyzed successfully! "
                    f"{len(detected)} skills detected. ✅"
                )

                st.rerun()

            else:

                st.error(
                    "No readable text found in this PDF."
                )


# ============================================================
# RESUME INTELLIGENCE
# ============================================================

if st.session_state.resume_result:

    result = st.session_state.resume_result

    detected_skills = result.get(
        "skills",
        []
    )

    st.markdown(
        "## 🧠 Resume Intelligence"
    )

    r1, r2, r3 = st.columns(3)

    with r1:

        st.metric(
            "Skills Detected",
            len(detected_skills)
        )

    with r2:

        completeness = min(
            100,
            round(
                (len(detected_skills) / len(ALL_SKILLS)) * 100
            )
        )

        st.metric(
            "Profile Completeness",
            f"{completeness}%"
        )

    with r3:

        st.metric(
            "Target Role",
            target_role
        )


    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 🔎 Detected Skills"
    )

    if detected_skills:

        html = ""

        for skill in detected_skills:

            html += (
                f'<span class="skill-tag">'
                f'✓ {escape(skill)}'
                f'</span>'
            )

        st.markdown(
            html,
            unsafe_allow_html=True
        )

    else:

        st.warning(
            "No supported technical skills detected."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# CURRENT SKILLS
# ============================================================

st.markdown(
    "## 🛠️ Current Skills"
)

if current_skills:

    html = ""

    for skill in current_skills:

        html += (
            f'<span class="skill-tag">'
            f'{escape(skill)}'
            f'</span>'
        )

    st.markdown(
        html,
        unsafe_allow_html=True
    )

else:

    st.info(
        "Select your current skills from the sidebar."
    )


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

st.markdown(
    "## 📊 Advanced Skill Gap Dashboard"
)

if st.button(
    "🔎 Analyze My Skill Gap",
    use_container_width=True
):

    if not current_skills:

        st.warning(
            "Please select at least one current skill."
        )

    else:

        payload = {

            "target_role": target_role,

            "skills": current_skills
        }

        try:

            response = requests.post(
                f"{BACKEND_URL}/analyze",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:

                st.session_state.skill_result = (
                    response.json()
                )

                st.session_state.ai_recommendation_result = None

                st.session_state.roadmap_result = None

                st.success(
                    "Skill gap analysis completed! ✅"
                )

                st.rerun()

            else:

                st.error(
                    f"Skill analysis failed: "
                    f"{response.status_code}"
                )

        except Exception as e:

            st.error(
                f"Connection error: {e}"
            )


# ============================================================
# SKILL GAP RESULT
# ============================================================

if st.session_state.skill_result:

    data = st.session_state.skill_result

    required_count = data.get(
        "required_count",
        0
    )

    matched_count = data.get(
        "matched_count",
        0
    )

    missing_count = data.get(
        "missing_count",
        0
    )

    score = data.get(
        "score",
        0
    )

    level = data.get(
        "level",
        "Unknown"
    )

    matched_skills = data.get(
        "matched_skills",
        []
    )

    missing_skills = data.get(
        "missing_skills",
        []
    )


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.metric(
            "Required Skills",
            required_count
        )

    with s2:

        st.metric(
            "Matched Skills",
            matched_count
        )

    with s3:

        st.metric(
            "Missing Skills",
            missing_count
        )

    with s4:

        st.metric(
            "Skill Match Score",
            f"{score}%"
        )


    # --------------------------------------------------------
    # CAREER READINESS
    # --------------------------------------------------------

    st.markdown(
        "### 🚀 Career Readiness"
    )

    st.progress(
        max(
            0.0,
            min(
                1.0,
                score / 100
            )
        )
    )

    st.write(
        f"**Current Level:** {level}"
    )


    # --------------------------------------------------------
    # MATCHED
    # --------------------------------------------------------

    st.markdown(
        "### ✅ Matched Skills"
    )

    if matched_skills:

        html = ""

        for skill in matched_skills:

            html += (
                f'<span class="skill-tag">'
                f'✓ {escape(skill)}'
                f'</span>'
            )

        st.markdown(
            html,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No matched skills."
        )


    # --------------------------------------------------------
    # MISSING
    # --------------------------------------------------------

    st.markdown(
        "### ⚠️ Missing Skills"
    )

    if missing_skills:

        html = ""

        for skill in missing_skills:

            html += (
                f'<span class="missing-tag">'
                f'⚠️ {escape(skill)}'
                f'</span>'
            )

        st.markdown(
            html,
            unsafe_allow_html=True
        )

    else:

        st.success(
            "No missing skills."
        )


    # --------------------------------------------------------
    # FIX 2:
    # STABLE SKILL GAP GRAPH
    # --------------------------------------------------------

    st.markdown(
        "### 📊 Skill Gap Overview"
    )

    chart_data = pd.DataFrame(
        {
            "Category": [
                "Matched Skills",
                "Missing Skills"
            ],

            "Skills": [
                matched_count,
                missing_count
            ]
        }
    )

    # Native Streamlit chart.
    # This avoids the SVG/Plotly rendering issue.

    st.bar_chart(
        chart_data.set_index("Category"),
        height=350
    )


# ============================================================
# AI RECOMMENDATIONS
# ============================================================

if st.session_state.skill_result:

    st.markdown(
        "## 🤖 AI Career Recommendations"
    )

    if st.button(
        "✨ Generate AI Recommendations",
        use_container_width=True
    ):

        missing_skills = (
            st.session_state.skill_result.get(
                "missing_skills",
                []
            )
        )

        payload = {

            "target_role": target_role,

            "missing_skills": missing_skills
        }

        try:

            response = requests.post(
                f"{BACKEND_URL}/ai-recommendation",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:

                st.session_state.ai_recommendation_result = (
                    response.json()
                )

                st.success(
                    "AI recommendations generated! 🤖"
                )

            else:

                st.error(
                    f"Recommendation failed: "
                    f"{response.status_code}"
                )

        except Exception as e:

            st.error(
                f"Connection error: {e}"
            )


# ============================================================
# SHOW AI RECOMMENDATIONS
# ============================================================

if st.session_state.ai_recommendation_result:

    recommendation_data = (
        st.session_state.ai_recommendation_result
    )

    recommendations = recommendation_data

    if isinstance(
        recommendation_data,
        dict
    ):

        recommendations = recommendation_data.get(
            "recommendations",
            recommendation_data.get(
                "data",
                []
            )
        )

    if isinstance(
        recommendations,
        list
    ):

        st.write(
            f"AI found {len(recommendations)} recommended skills."
        )

        for index, item in enumerate(
            recommendations,
            start=1
        ):

            if not isinstance(
                item,
                dict
            ):

                continue

            skill = item.get(
                "skill",
                item.get(
                    "topic",
                    "Skill"
                )
            )

            priority = item.get(
                "priority",
                "Recommended"
            )

            estimated_time = item.get(
                "estimated_time",
                item.get(
                    "duration",
                    "Not specified"
                )
            )

            reason = item.get(
                "reason",
                ""
            )

            action = item.get(
                "action",
                ""
            )

            st.markdown(
                f"""
                <div class="recommendation-card">

                <h3>
                #{index} — {escape(str(skill))}
                </h3>

                <p>
                <b>Priority:</b>
                {escape(str(priority))}
                &nbsp;&nbsp;&nbsp;

                <b>Estimated Time:</b>
                {escape(str(estimated_time))}
                </p>

                <p>
                <b>Why learn it?</b><br>
                {escape(str(reason))}
                </p>

                <p>
                <b>What to practice?</b><br>
                {escape(str(action))}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# PERSONALIZED ROADMAP
# ============================================================

if st.session_state.skill_result:

    st.markdown(
        "## 🗺️ Personalized Learning Roadmap"
    )

    if st.button(
        "🛣️ Generate Learning Roadmap",
        use_container_width=True
    ):

        missing_skills = (
            st.session_state.skill_result.get(
                "missing_skills",
                []
            )
        )

        payload = {

            "target_role": target_role,

            "missing_skills": missing_skills
        }

        try:

            response = requests.post(
                f"{BACKEND_URL}/roadmap",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:

                st.session_state.roadmap_result = (
                    response.json()
                )

                st.success(
                    "Learning roadmap generated! 🗺️"
                )

            else:

                st.error(
                    f"Roadmap failed: "
                    f"{response.status_code}"
                )

        except Exception as e:

            st.error(
                f"Connection error: {e}"
            )


# ============================================================
# SHOW ROADMAP
# ============================================================

if st.session_state.roadmap_result:

    roadmap_data = (
        st.session_state.roadmap_result
    )

    if isinstance(
        roadmap_data,
        dict
    ):

        roadmap = roadmap_data.get(
            "roadmap",
            roadmap_data.get(
                "learning_roadmap",
                []
            )
        )

    else:

        roadmap = roadmap_data


    if isinstance(
        roadmap,
        list
    ):

        for index, item in enumerate(
            roadmap,
            start=1
        ):

            if not isinstance(
                item,
                dict
            ):

                continue

            skill = item.get(
                "skill",
                item.get(
                    "topic",
                    "Learning Topic"
                )
            )

            duration = item.get(
                "duration",
                item.get(
                    "estimated_time",
                    "Not specified"
                )
            )

            action = item.get(
                "action",
                item.get(
                    "description",
                    "Learn and practice this topic."
                )
            )

            st.markdown(
                f"""
                <div class="roadmap-card">

                <h3>
                Step {index}: {escape(str(skill))}
                </h3>

                <p>
                ⏱️ <b>{escape(str(duration))}</b>
                </p>

                <p>
                {escape(str(action))}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# JOB DESCRIPTION MATCHER
# ============================================================

st.markdown(
    "## 💼 Job Description Matcher"
)

st.markdown(
    """
    <div class="card">

    <p>
    Paste a job description below to compare the technical
    skills required by the job with the skills detected
    from your resume.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

job_description = st.text_area(
    "📋 Paste Job Description here",
    height=220,
    placeholder=(
        "Example:\n\n"
        "We are looking for a Data Analyst with Python, SQL, "
        "Excel, Power BI, Statistics and Pandas."
    ),
    key="job_description_input"
)


# ============================================================
# FIX 3:
# LOCAL JOB MATCHING
# NO /job-match ENDPOINT REQUIRED
# ============================================================

if st.button(
    "🔎 Match Resume With Job Description",
    use_container_width=True
):

    if not st.session_state.resume_text:

        st.warning(
            "Please upload and analyze your resume first."
        )

    elif not job_description.strip():

        st.warning(
            "Please paste a job description first."
        )

    else:

        result = calculate_job_match(
            st.session_state.resume_text,
            job_description
        )

        st.session_state.job_match_result = result

        st.success(
            "Job description analyzed successfully! ✅"
        )

        st.rerun()


# ============================================================
# JOB MATCH RESULT
# ============================================================

if st.session_state.job_match_result:

    job_data = st.session_state.job_match_result

    match_percentage = job_data.get(
        "match_percentage",
        0
    )

    match_level = job_data.get(
        "match_level",
        "Low Match"
    )

    matched_job_skills = job_data.get(
        "matched_skills",
        []
    )

    missing_job_skills = job_data.get(
        "missing_skills",
        []
    )

    job_skills = job_data.get(
        "job_skills",
        []
    )


    st.markdown(
        "### 📋 Job Match Result"
    )


    j1, j2 = st.columns(2)

    with j1:

        st.metric(
            "Match Percentage",
            f"{match_percentage}%"
        )

    with j2:

        st.metric(
            "Match Level",
            match_level
        )


    # --------------------------------------------------------
    # JOB SKILLS
    # --------------------------------------------------------

    st.markdown(
        "### 🔎 Skills Found in Job Description"
    )

    if job_skills:

        html = ""

        for skill in job_skills:

            html += (
                f'<span class="skill-tag">'
                f'✓ {escape(skill)}'
                f'</span>'
            )

        st.markdown(
            html,
            unsafe_allow_html=True
        )

    else:

        st.warning(
            "No supported technical skills were detected "
            "in this job description."
        )


    # --------------------------------------------------------
    # MATCHED
    # --------------------------------------------------------

    st.markdown(
        "### ✅ Matched Skills"
    )

    if matched_job_skills:

        html = ""

        for skill in matched_job_skills:

            html += (
                f'<span class="skill-tag">'
                f'✓ {escape(skill)}'
                f'</span>'
            )

        st.markdown(
            html,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No matched skills."
        )


    # --------------------------------------------------------
    # MISSING
    # --------------------------------------------------------

    st.markdown(
        "### ⚠️ Missing Skills"
    )

    if missing_job_skills:

        html = ""

        for skill in missing_job_skills:

            html += (
                f'<span class="missing-tag">'
                f'⚠️ {escape(skill)}'
                f'</span>'
            )

        st.markdown(
            html,
            unsafe_allow_html=True
        )

    else:

        st.success(
            "No missing technical skills."
        )


# ============================================================
# PDF REPORT
# ============================================================

def generate_pdf_report(
    student_name,
    course,
    target_role,
    resume_result,
    skill_result,
    ai_result,
    roadmap_result,
    job_result
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        leading=28,
        spaceAfter=12
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=20,
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15
    )

    footer_style = ParagraphStyle(
        "Footer",
        parent=normal_style,
        alignment=TA_CENTER,
        fontSize=8
    )

    story = []


    story.append(
        Paragraph(
            "AI Skill-Gap Analyzer",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Personalized Career Intelligence Report",
            footer_style
        )
    )

    story.append(
        Spacer(1, 12)
    )


    # PROFILE

    story.append(
        Paragraph(
            "Student Profile",
            heading_style
        )
    )

    profile_data = [

        [
            Paragraph(
                "<b>Name</b>",
                normal_style
            ),

            Paragraph(
                escape(student_name or "Not provided"),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Course</b>",
                normal_style
            ),

            Paragraph(
                escape(course or "Not provided"),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Target Role</b>",
                normal_style
            ),

            Paragraph(
                escape(target_role),
                normal_style
            )
        ]
    ]

    profile_table = Table(
        profile_data,
        colWidths=[
            45 * mm,
            120 * mm
        ]
    )

    profile_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    story.append(
        profile_table
    )

    story.append(
        Spacer(1, 12)
    )


    # RESUME

    story.append(
        Paragraph(
            "Resume Analysis",
            heading_style
        )
    )

    resume_skills = []

    if resume_result:

        resume_skills = resume_result.get(
            "skills",
            []
        )

    story.append(
        Paragraph(
            "<b>Detected Skills:</b> "
            + escape(
                ", ".join(resume_skills)
                if resume_skills
                else "None"
            ),
            normal_style
        )
    )


    # SKILL GAP

    if skill_result:

        story.append(
            Paragraph(
                "Skill Gap Analysis",
                heading_style
            )
        )

        score = skill_result.get(
            "score",
            0
        )

        level = skill_result.get(
            "level",
            "Unknown"
        )

        required = skill_result.get(
            "required_count",
            0
        )

        matched = skill_result.get(
            "matched_count",
            0
        )

        missing = skill_result.get(
            "missing_count",
            0
        )

        matched_skills = skill_result.get(
            "matched_skills",
            []
        )

        missing_skills = skill_result.get(
            "missing_skills",
            []
        )

        table_data = [

            ["Skill Match", f"{score}%"],

            ["Level", str(level)],

            ["Required Skills", str(required)],

            ["Matched Skills", str(matched)],

            ["Missing Skills", str(missing)]
        ]

        score_table = Table(
            table_data,
            colWidths=[
                70 * mm,
                95 * mm
            ]
        )

        score_table.setStyle(
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),

                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.lightgrey
                    ),

                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    )
                ]
            )
        )

        story.append(
            score_table
        )

        story.append(
            Spacer(1, 8)
        )

        story.append(
            Paragraph(
                "<b>Matched:</b> "
                + escape(
                    ", ".join(matched_skills)
                    if matched_skills
                    else "None"
                ),
                normal_style
            )
        )

        story.append(
            Paragraph(
                "<b>Missing:</b> "
                + escape(
                    ", ".join(missing_skills)
                    if missing_skills
                    else "None"
                ),
                normal_style
            )
        )


    # AI RECOMMENDATIONS

    if ai_result:

        story.append(
            PageBreak()
        )

        story.append(
            Paragraph(
                "AI Recommendations",
                heading_style
            )
        )

        recommendations = ai_result

        if isinstance(
            ai_result,
            dict
        ):

            recommendations = ai_result.get(
                "recommendations",
                ai_result.get(
                    "data",
                    []
                )
            )

        if isinstance(
            recommendations,
            list
        ):

            for item in recommendations:

                if not isinstance(
                    item,
                    dict
                ):

                    continue

                skill = item.get(
                    "skill",
                    item.get(
                        "topic",
                        "Skill"
                    )
                )

                priority = item.get(
                    "priority",
                    "Recommended"
                )

                duration = item.get(
                    "estimated_time",
                    item.get(
                        "duration",
                        "Not specified"
                    )
                )

                reason = item.get(
                    "reason",
                    ""
                )

                action = item.get(
                    "action",
                    ""
                )

                story.append(
                    Paragraph(
                        f"<b>{escape(str(skill))}</b>",
                        normal_style
                    )
                )

                story.append(
                    Paragraph(
                        f"Priority: {escape(str(priority))}",
                        normal_style
                    )
                )

                story.append(
                    Paragraph(
                        f"Estimated Time: "
                        f"{escape(str(duration))}",
                        normal_style
                    )
                )

                story.append(
                    Paragraph(
                        f"Why: {escape(str(reason))}",
                        normal_style
                    )
                )

                story.append(
                    Paragraph(
                        f"Action: {escape(str(action))}",
                        normal_style
                    )
                )

                story.append(
                    Spacer(1, 8)
                )


    # ROADMAP

    if roadmap_result:

        story.append(
            Paragraph(
                "Personalized Learning Roadmap",
                heading_style
            )
        )

        roadmap = roadmap_result

        if isinstance(
            roadmap_result,
            dict
        ):

            roadmap = roadmap_result.get(
                "roadmap",
                roadmap_result.get(
                    "learning_roadmap",
                    []
                )
            )

        if isinstance(
            roadmap,
            list
        ):

            for index, item in enumerate(
                roadmap,
                start=1
            ):

                if not isinstance(
                    item,
                    dict
                ):

                    continue

                skill = item.get(
                    "skill",
                    item.get(
                        "topic",
                        "Topic"
                    )
                )

                duration = item.get(
                    "duration",
                    item.get(
                        "estimated_time",
                        "Not specified"
                    )
                )

                action = item.get(
                    "action",
                    item.get(
                        "description",
                        ""
                    )
                )

                story.append(
                    Paragraph(
                        f"<b>Step {index}: "
                        f"{escape(str(skill))}</b>",
                        normal_style
                    )
                )

                story.append(
                    Paragraph(
                        f"Duration: "
                        f"{escape(str(duration))}",
                        normal_style
                    )
                )

                story.append(
                    Paragraph(
                        escape(str(action)),
                        normal_style
                    )
                )

                story.append(
                    Spacer(1, 8)
                )


    # JOB MATCH

    if job_result:

        story.append(
            Paragraph(
                "Job Description Match",
                heading_style
            )
        )

        percentage = job_result.get(
            "match_percentage",
            0
        )

        level = job_result.get(
            "match_level",
            "Unknown"
        )

        matched = job_result.get(
            "matched_skills",
            []
        )

        missing = job_result.get(
            "missing_skills",
            []
        )

        story.append(
            Paragraph(
                f"<b>Match Percentage:</b> "
                f"{percentage}%",
                normal_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Match Level:</b> "
                f"{escape(str(level))}",
                normal_style
            )
        )

        story.append(
            Paragraph(
                "<b>Matched Skills:</b> "
                + escape(
                    ", ".join(matched)
                    if matched
                    else "None"
                ),
                normal_style
            )
        )

        story.append(
            Paragraph(
                "<b>Missing Skills:</b> "
                + escape(
                    ", ".join(missing)
                    if missing
                    else "None"
                ),
                normal_style
            )
        )


    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            "Generated by AI Skill-Gap Analyzer",
            footer_style
        )
    )

    document.build(
        story
    )

    buffer.seek(0)

    return buffer


# ============================================================
# PROFESSIONAL PDF REPORT
# ============================================================

if st.session_state.resume_result:

    st.markdown(
        "## 📄 Professional PDF Report"
    )

    st.markdown(
        """
        <div class="card">

        Generate a professional PDF containing your complete
        resume analysis, skill gap, AI recommendations,
        personalized roadmap and job match.

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "📥 Generate Professional PDF Report",
        use_container_width=True
    ):

        pdf_file = generate_pdf_report(

            student_name=student_name,

            course=course,

            target_role=target_role,

            resume_result=st.session_state.resume_result,

            skill_result=st.session_state.skill_result,

            ai_result=st.session_state.ai_recommendation_result,

            roadmap_result=st.session_state.roadmap_result,

            job_result=st.session_state.job_match_result
        )

        st.download_button(

            "⬇️ Download Career Report",

            data=pdf_file,

            file_name="AI_Skill_Gap_Career_Report.pdf",

            mime="application/pdf",

            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br><br>

    <div style="
        text-align:center;
        color:#667085;
        padding:20px;
        font-size:13px;
    ">

    🎯 <b>AI Skill-Gap Analyzer</b>

    <br><br>

    Resume Intelligence • Skill Gap Detection •
    AI Recommendations • Personalized Roadmap •
    Job Description Matching • PDF Report

    </div>
    """,
    unsafe_allow_html=True
)