from html import escape
from io import BytesIO

import plotly.express as px
import requests
import streamlit as st
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

# =========================================================
# CONFIG
# =========================================================

BACKEND_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="AI Skill-Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    padding: 22px;
    border-radius: 15px;
    background: rgba(128,128,128,0.08);
    border: 1px solid rgba(128,128,128,0.18);
    margin-bottom: 15px;
}

.metric-card {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    background: rgba(128,128,128,0.08);
    border: 1px solid rgba(128,128,128,0.18);
}

.metric-title {
    font-size: 15px;
    color: #777;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
}

.success-box {
    padding: 15px;
    border-radius: 10px;
    background: rgba(0,180,80,0.10);
    border: 1px solid rgba(0,180,80,0.25);
}

.section-title {
    font-size: 26px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 15px;
}

.skill-tag {
    display: inline-block;
    padding: 7px 12px;
    margin: 4px;
    border-radius: 20px;
    background: rgba(100,100,100,0.12);
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_result" not in st.session_state:
    st.session_state.resume_result = None

if "skill_result" not in st.session_state:
    st.session_state.skill_result = None

if "roadmap_result" not in st.session_state:
    st.session_state.roadmap_result = None

if "job_match_result" not in st.session_state:
    st.session_state.job_match_result = None

if "ai_recommendation_result" not in st.session_state:
    st.session_state.ai_recommendation_result = None


# =========================================================
# SKILLS
# =========================================================

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


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_pdf_text(uploaded_file):

    text = ""

    try:
        reader = PdfReader(uploaded_file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:

        st.error(f"PDF reading error: {e}")

    return text


# =========================================================
# SKILL DETECTION
# =========================================================

def detect_skills(text):

    detected = []

    text_lower = text.lower()

    aliases = {
        "Python": ["python"],
        "SQL": ["sql", "mysql", "postgresql", "database"],
        "Excel": ["excel", "microsoft excel"],
        "Power BI": ["power bi", "powerbi"],
        "Statistics": ["statistics", "statistical"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Machine Learning": ["machine learning", "ml"],
        "Scikit-learn": ["scikit-learn", "sklearn"],
        "Java": ["java"],
        "Data Structures": ["data structures", "dsa"],
        "Algorithms": ["algorithms"],
        "Git": ["git", "github", "gitlab"],
        "OOP": ["oop", "object oriented"],
        "ETL": ["etl"],
        "Apache Spark": ["apache spark", "spark"],
        "Cloud": ["cloud", "aws", "azure", "gcp"],
        "HTML": ["html"],
        "CSS": ["css"],
        "JavaScript": ["javascript", "js"],
        "React": ["react"]
    }

    for skill, words in aliases.items():

        for word in words:

            if word in text_lower:

                detected.append(skill)
                break

    return detected


# =========================================================
# PROFESSIONAL PDF REPORT GENERATOR
# =========================================================

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

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=18
    )

    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        spaceAfter=5
    )

    small_style = ParagraphStyle(
        "SmallCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12
    )

    story = []

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "AI SKILL-GAP ANALYZER",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Resume Intelligence & Personalized Career Report",
            subtitle_style
        )
    )

    # -----------------------------------------------------
    # STUDENT INFORMATION
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "STUDENT PROFILE",
            heading_style
        )
    )

    profile_data = [
        [
            Paragraph("<b>Student Name</b>", small_style),
            Paragraph(escape(student_name or "Not Provided"), small_style)
        ],
        [
            Paragraph("<b>Course</b>", small_style),
            Paragraph(escape(course or "Not Provided"), small_style)
        ],
        [
            Paragraph("<b>Target Role</b>", small_style),
            Paragraph(escape(target_role), small_style)
        ]
    ]

    profile_table = Table(
        profile_data,
        colWidths=[45 * mm, 120 * mm]
    )

    profile_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ])
    )

    story.append(profile_table)
    story.append(Spacer(1, 8))

    # -----------------------------------------------------
    # RESUME ANALYSIS
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "RESUME ANALYSIS",
            heading_style
        )
    )

    detected_skills = []

    if resume_result:

        detected_skills = resume_result.get(
            "skills",
            []
        )

    story.append(
        Paragraph(
            f"<b>Skills Detected:</b> {len(detected_skills)}",
            body_style
        )
    )

    story.append(
        Paragraph(
            "<b>Detected Skills:</b> " +
            escape(", ".join(detected_skills) if detected_skills else "None"),
            body_style
        )
    )

    # -----------------------------------------------------
    # SKILL GAP
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "SKILL GAP ANALYSIS",
            heading_style
        )
    )

    skill_data = skill_result or {}

    score = skill_data.get(
        "score",
        0
    )

    level = skill_data.get(
        "level",
        "Not Available"
    )

    matched_skills = skill_data.get(
        "matched_skills",
        []
    )

    missing_skills = skill_data.get(
        "missing_skills",
        []
    )

    required_count = skill_data.get(
        "required_count",
        len(matched_skills) + len(missing_skills)
    )

    story.append(
        Paragraph(
            f"<b>Skill Match Score:</b> {score}%",
            body_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Career Level:</b> {escape(str(level))}",
            body_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Required Skills:</b> {required_count}",
            body_style
        )
    )

    story.append(
        Paragraph(
            "<b>Matched Skills:</b> " +
            escape(", ".join(matched_skills) if matched_skills else "None"),
            body_style
        )
    )

    story.append(
        Paragraph(
            "<b>Missing Skills:</b> " +
            escape(", ".join(missing_skills) if missing_skills else "None"),
            body_style
        )
    )

    # -----------------------------------------------------
    # SCORE TABLE
    # -----------------------------------------------------

    score_table_data = [
        [
            Paragraph("<b>Metric</b>", small_style),
            Paragraph("<b>Value</b>", small_style)
        ],
        [
            Paragraph("Skill Match Score", small_style),
            Paragraph(f"{score}%", small_style)
        ],
        [
            Paragraph("Matched Skills", small_style),
            Paragraph(str(len(matched_skills)), small_style)
        ],
        [
            Paragraph("Missing Skills", small_style),
            Paragraph(str(len(missing_skills)), small_style)
        ]
    ]

    score_table = Table(
        score_table_data,
        colWidths=[95 * mm, 70 * mm]
    )

    score_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (1, 1), (1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ])
    )

    story.append(Spacer(1, 7))
    story.append(score_table)

    # -----------------------------------------------------
    # AI RECOMMENDATIONS
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "AI CAREER RECOMMENDATIONS",
            heading_style
        )
    )

    recommendations = []

    if ai_result:

        recommendations = ai_result.get(
            "recommendations",
            []
        )

    if recommendations:

        for index, item in enumerate(
            recommendations,
            start=1
        ):

            skill = item.get(
                "skill",
                "Unknown"
            )

            priority = item.get(
                "priority",
                "Medium"
            )

            estimated_time = item.get(
                "estimated_time",
                "1-2 weeks"
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
                    f"<b>{index}. {escape(str(skill))}</b>",
                    body_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Priority:</b> {escape(str(priority))} "
                    f"&nbsp;&nbsp; "
                    f"<b>Estimated Time:</b> {escape(str(estimated_time))}",
                    small_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Reason:</b> {escape(str(reason))}",
                    small_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Action:</b> {escape(str(action))}",
                    small_style
                )
            )

            story.append(Spacer(1, 6))

    else:

        story.append(
            Paragraph(
                "Generate AI recommendations from the dashboard to include them in this report.",
                body_style
            )
        )

    # -----------------------------------------------------
    # ROADMAP
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "PERSONALIZED LEARNING ROADMAP",
            heading_style
        )
    )

    roadmap_items = []

    if roadmap_result:

        if isinstance(roadmap_result, dict):

            roadmap_items = roadmap_result.get(
                "roadmap",
                roadmap_result.get(
                    "learning_roadmap",
                    []
                )
            )

        elif isinstance(roadmap_result, list):

            roadmap_items = roadmap_result

    if roadmap_items:

        for i, item in enumerate(
            roadmap_items,
            start=1
        ):

            if isinstance(item, dict):

                skill = item.get(
                    "skill",
                    item.get(
                        "topic",
                        f"Step {i}"
                    )
                )

                duration = item.get(
                    "duration",
                    item.get(
                        "estimated_time",
                        ""
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
                        f"<b>Step {i}: {escape(str(skill))}</b>",
                        body_style
                    )
                )

                if duration:

                    story.append(
                        Paragraph(
                            f"<b>Duration:</b> {escape(str(duration))}",
                            small_style
                        )
                    )

                if action:

                    story.append(
                        Paragraph(
                            escape(str(action)),
                            small_style
                        )
                    )

            else:

                story.append(
                    Paragraph(
                        f"<b>Step {i}:</b> {escape(str(item))}",
                        body_style
                    )
                )

            story.append(Spacer(1, 5))

    else:

        if missing_skills:

            story.append(
                Paragraph(
                    "Recommended learning order: " +
                    escape(" → ".join(missing_skills)),
                    body_style
                )
            )

        else:

            story.append(
                Paragraph(
                    "No learning roadmap generated yet.",
                    body_style
                )
            )

    # -----------------------------------------------------
    # JOB MATCH
    # -----------------------------------------------------

    if job_result:

        story.append(
            Paragraph(
                "JOB DESCRIPTION MATCH",
                heading_style
            )
        )

        match_percentage = job_result.get(
            "match_percentage",
            0
        )

        match_level = job_result.get(
            "match_level",
            "Low Match"
        )

        job_matched = job_result.get(
            "matched_skills",
            []
        )

        job_missing = job_result.get(
            "missing_skills",
            []
        )

        story.append(
            Paragraph(
                f"<b>Match Percentage:</b> {match_percentage}%",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Match Level:</b> {escape(str(match_level))}",
                body_style
            )
        )

        story.append(
            Paragraph(
                "<b>Matched Skills:</b> " +
                escape(", ".join(job_matched) if job_matched else "None"),
                body_style
            )
        )

        story.append(
            Paragraph(
                "<b>Missing Skills:</b> " +
                escape(", ".join(job_missing) if job_missing else "None"),
                body_style
            )
        )

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Generated by AI Skill-Gap Analyzer",
            subtitle_style
        )
    )

    # -----------------------------------------------------
    # BUILD PDF
    # -----------------------------------------------------

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎯 AI Skill-Gap Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered Resume Analysis • Skill Gap Detection • Career Roadmap</div>',
    unsafe_allow_html=True
)


# =========================================================
# BACKEND STATUS
# =========================================================

try:

    response = requests.get(
        BACKEND_URL,
        timeout=3
    )

    if response.status_code == 200:

        st.markdown(
            '<div class="success-box">🟢 Backend Connected Successfully</div>',
            unsafe_allow_html=True
        )

    else:

        st.warning(
            "Backend is responding but returned an unexpected status."
        )

except Exception:

    st.error(
        "🔴 Backend is not connected. Please start Flask backend first."
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Profile")

    student_name = st.text_input(
        "Student Name",
        placeholder="Enter your name"
    )

    course = st.text_input(
        "Course",
        placeholder="Example: B.Tech CSE"
    )

    target_role = st.selectbox(
        "Target Job Role",
        [
            "Data Analyst",
            "Data Scientist",
            "Software Developer",
            "Data Engineer",
            "Web Developer"
        ]
    )

    st.markdown("---")

    st.info(
        "Upload your resume and analyze your current skills against your target role."
    )


# =========================================================
# RESUME ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">📄 Resume Analysis</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    if st.button(
        "🔍 Analyze My Resume",
        use_container_width=True
    ):

        with st.spinner(
            "Reading and analyzing resume..."
        ):

            resume_text = extract_pdf_text(
                uploaded_file
            )

            st.session_state.resume_text = resume_text

            detected = detect_skills(
                resume_text
            )

            st.session_state.resume_result = {
                "skills": detected,
                "text": resume_text
            }

        st.success(
            "Resume analyzed successfully! ✅"
        )


# =========================================================
# RESUME INTELLIGENCE
# =========================================================

if st.session_state.resume_result:

    result = st.session_state.resume_result

    detected_skills = result["skills"]

    st.markdown(
        '<div class="section-title">🧠 Resume Intelligence</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Skills Detected</div>
                <div class="metric-value">{len(detected_skills)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        completeness = min(
            100,
            int(
                (
                    len(detected_skills)
                    / max(len(ALL_SKILLS), 1)
                ) * 100
            )
        )

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Profile Completeness</div>
                <div class="metric-value">{completeness}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Target Role</div>
                <div class="metric-value" style="font-size:20px;">
                    {target_role}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    if detected_skills:

        st.markdown("**Detected Skills**")

        skill_html = ""

        for skill in detected_skills:

            skill_html += (
                f'<span class="skill-tag">✓ {skill}</span>'
            )

        st.markdown(
            skill_html,
            unsafe_allow_html=True
        )

    else:

        st.warning(
            "No known technical skills were detected."
        )


# =========================================================
# CURRENT SKILLS
# =========================================================

st.markdown(
    '<div class="section-title">🛠️ Current Skills</div>',
    unsafe_allow_html=True
)

default_skills = []

if st.session_state.resume_result:

    default_skills = st.session_state.resume_result["skills"]

current_skills = st.multiselect(
    "Select your current skills",
    ALL_SKILLS,
    default=default_skills
)


# =========================================================
# SKILL GAP ANALYSIS
# =========================================================

if st.button(
    "🎯 Analyze My Skill Gap",
    use_container_width=True
):

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

            st.session_state.skill_result = response.json()

        else:

            st.error(
                f"Skill analysis failed: {response.status_code}"
            )

    except Exception as e:

        st.error(
            f"Connection error: {e}"
        )


# =========================================================
# SKILL GAP DASHBOARD
# =========================================================

if st.session_state.skill_result:

    data = st.session_state.skill_result

    st.markdown(
        '<div class="section-title">📊 Advanced Skill Gap Dashboard</div>',
        unsafe_allow_html=True
    )

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
        "Needs Improvement"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Required Skills</div>
                <div class="metric-value">{required_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Matched Skills</div>
                <div class="metric-value">{matched_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Missing Skills</div>
                <div class="metric-value">{missing_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Skill Match Score</div>
                <div class="metric-value">{score}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.subheader("🚀 Career Readiness")

    st.progress(
        min(
            max(float(score) / 100, 0),
            1
        )
    )

    st.write(
        f"**Current Level:** {level}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="card"><h3>✅ Matched Skills</h3>',
            unsafe_allow_html=True
        )

        matched_skills = data.get(
            "matched_skills",
            []
        )

        if matched_skills:

            for skill in matched_skills:

                st.write(
                    f"✅ {skill}"
                )

        else:

            st.write(
                "No matched skills."
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            '<div class="card"><h3>⚠️ Missing Skills</h3>',
            unsafe_allow_html=True
        )

        missing_skills = data.get(
            "missing_skills",
            []
        )

        if missing_skills:

            for skill in missing_skills:

                st.write(
                    f"⚠️ {skill}"
                )

        else:

            st.write(
                "No major skill gaps detected."
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # Chart

    chart_data = {
        "Category": [
            "Matched Skills",
            "Missing Skills"
        ],
        "Skills": [
            matched_count,
            missing_count
        ]
    }

    fig = px.bar(
        chart_data,
        x="Category",
        y="Skills",
        title="Skill Gap Overview",
        text="Skills"
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# AI RECOMMENDATIONS
# =========================================================

if st.session_state.skill_result:

    st.markdown(
        '<div class="section-title">🤖 AI Career Recommendations</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "🚀 Generate AI Recommendations",
        use_container_width=True
    ):

        missing_skills = st.session_state.skill_result.get(
            "missing_skills",
            []
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

                st.session_state.ai_recommendation_result = response.json()

            else:

                st.error(
                    f"Recommendation failed: {response.status_code}"
                )

        except Exception as e:

            st.error(
                f"Connection error: {e}"
            )


# =========================================================
# DISPLAY AI RECOMMENDATIONS
# =========================================================

if st.session_state.ai_recommendation_result:

    ai_data = st.session_state.ai_recommendation_result

    recommendations = ai_data.get(
        "recommendations",
        []
    )

    if recommendations:

        st.success(
            f"AI found {len(recommendations)} recommended skills."
        )

        for index, item in enumerate(
            recommendations,
            start=1
        ):

            skill = item.get(
                "skill",
                "Unknown"
            )

            priority = item.get(
                "priority",
                "Medium"
            )

            estimated_time = item.get(
                "estimated_time",
                "1-2 weeks"
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
                <div class="card">

                <h3>#{index} — {escape(str(skill))}</h3>

                <b>Priority:</b> {escape(str(priority))}
                &nbsp;&nbsp;&nbsp;
                <b>Estimated Time:</b> {escape(str(estimated_time))}

                <br><br>

                <b>Why learn it?</b><br>
                {escape(str(reason))}

                <br><br>

                <b>What to practice?</b><br>
                {escape(str(action))}

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# ROADMAP
# =========================================================

if st.session_state.skill_result:

    st.markdown(
        '<div class="section-title">🗺️ Personalized Learning Roadmap</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "📚 Generate Learning Roadmap",
        use_container_width=True
    ):

        missing_skills = st.session_state.skill_result.get(
            "missing_skills",
            []
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

                st.session_state.roadmap_result = response.json()

            else:

                st.error(
                    f"Roadmap generation failed: {response.status_code}"
                )

        except Exception as e:

            st.error(
                f"Connection error: {e}"
            )


if st.session_state.roadmap_result:

    roadmap = st.session_state.roadmap_result

    if isinstance(roadmap, dict):

        roadmap_items = roadmap.get(
            "roadmap",
            roadmap.get(
                "learning_roadmap",
                []
            )
        )

    else:

        roadmap_items = roadmap

    if roadmap_items:

        for i, item in enumerate(
            roadmap_items,
            start=1
        ):

            if isinstance(item, dict):

                skill = item.get(
                    "skill",
                    item.get(
                        "topic",
                        f"Step {i}"
                    )
                )

                duration = item.get(
                    "duration",
                    item.get(
                        "estimated_time",
                        ""
                    )
                )

                action = item.get(
                    "action",
                    item.get(
                        "description",
                        ""
                    )
                )

                st.markdown(
                    f"""
                    <div class="card">
                    <b>Step {i}: {escape(str(skill))}</b><br>
                    ⏱️ {escape(str(duration))}<br>
                    {escape(str(action))}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.write(
                    f"**Step {i}:** {item}"
                )


# =========================================================
# JOB DESCRIPTION MATCHER
# =========================================================

st.markdown(
    '<div class="section-title">💼 Job Description Matcher</div>',
    unsafe_allow_html=True
)

job_description = st.text_area(
    "Paste Job Description here",
    height=220,
    placeholder="Paste the complete job description..."
)


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

        payload = {
            "resume_text": st.session_state.resume_text,
            "job_description": job_description
        }

        try:

            response = requests.post(
                f"{BACKEND_URL}/job-match",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:

                st.session_state.job_match_result = response.json()

            else:

                st.error(
                    f"Job matching failed: {response.status_code}"
                )

        except Exception as e:

            st.error(
                f"Connection error: {e}"
            )


# =========================================================
# JOB MATCH RESULT
# =========================================================

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

    matched = job_data.get(
        "matched_skills",
        []
    )

    missing = job_data.get(
        "missing_skills",
        []
    )

    st.markdown(
        '<div class="section-title">📋 Job Match Result</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Match Percentage",
            f"{match_percentage}%"
        )

    with c2:

        st.metric(
            "Match Level",
            match_level
        )

    st.progress(
        min(
            max(
                float(match_percentage) / 100,
                0
            ),
            1
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### ✅ Matched Skills"
        )

        if matched:

            for skill in matched:

                st.write(
                    f"✓ {skill}"
                )

        else:

            st.write(
                "No matched skills."
            )

    with col2:

        st.markdown(
            "### ⚠️ Missing Skills"
        )

        if missing:

            for skill in missing:

                st.write(
                    f"• {skill}"
                )

        else:

            st.write(
                "No missing skills."
            )


# =========================================================
# PROFESSIONAL PDF REPORT
# =========================================================

st.markdown(
    '<div class="section-title">📄 Professional PDF Report</div>',
    unsafe_allow_html=True
)

if st.session_state.skill_result:

    st.write(
        "Generate a professional PDF containing your complete analysis."
    )

    try:

        pdf_data = generate_pdf_report(
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
            label="📥 Download Professional PDF Report",
            data=pdf_data,
            file_name="AI_Skill_Gap_Professional_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"PDF generation error: {e}"
        )

else:

    st.info(
        "Complete Skill Gap Analysis first to generate the PDF report."
    )


# =========================================================
# RESET
# =========================================================

st.markdown("---")

if st.button(
    "🔄 Reset Analysis",
    use_container_width=True
):

    st.session_state.resume_text = ""
    st.session_state.resume_result = None
    st.session_state.skill_result = None
    st.session_state.roadmap_result = None
    st.session_state.job_match_result = None
    st.session_state.ai_recommendation_result = None

    st.rerun()