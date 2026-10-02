from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


# ============================================================
# SKILL DATABASE
# ============================================================

SKILLS = {
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
        "microsoft excel",
        "ms excel"
    ],
    "Power BI": [
        "power bi",
        "powerbi"
    ],
    "Statistics": [
        "statistics",
        "statistical analysis",
        "statistical"
    ],
    "Pandas": [
        "pandas"
    ],
    "NumPy": [
        "numpy"
    ],
    "Machine Learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],
    "Scikit-learn": [
        "scikit-learn",
        "sklearn"
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
        "object oriented programming",
        "object-oriented programming"
    ],
    "ETL": [
        "etl",
        "extract transform load"
    ],
    "Apache Spark": [
        "apache spark",
        "spark"
    ],
    "Cloud": [
        "cloud",
        "aws",
        "azure",
        "google cloud",
        "gcp"
    ],
    "HTML": [
        "html"
    ],
    "CSS": [
        "css"
    ],
    "JavaScript": [
        "javascript",
        "java script",
        "js"
    ],
    "React": [
        "react",
        "reactjs",
        "react.js"
    ]
}


# ============================================================
# ROLE REQUIRED SKILLS
# ============================================================

ROLE_SKILLS = {
    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Statistics",
        "Pandas"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Statistics",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "Scikit-learn"
    ],

    "Software Developer": [
        "Python",
        "Java",
        "Data Structures",
        "Algorithms",
        "Git",
        "SQL",
        "OOP"
    ],

    "Data Engineer": [
        "Python",
        "SQL",
        "ETL",
        "Data Structures",
        "Apache Spark",
        "Cloud",
        "Git"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Git",
        "SQL"
    ]
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_text(text):
    if not text:
        return ""

    text = text.lower()
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text)

    return text


def detect_skills(text):
    text = normalize_text(text)

    detected = []

    for skill, aliases in SKILLS.items():

        for alias in aliases:

            alias = normalize_text(alias)

            if alias in text:
                detected.append(skill)
                break

    return detected


def calculate_percentage(matched, required):
    if not required:
        return 0

    return round((len(matched) / len(required)) * 100, 2)


# ============================================================
# HOME
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "success",
        "message": "AI Skill-Gap Analyzer Backend is Running",
        "version": "2.0",
        "features": [
            "Resume Analysis",
            "Skill Gap Analysis",
            "Learning Roadmap",
            "Job Description Matcher",
            "AI Recommendations"
        ]
    })


# ============================================================
# RESUME ANALYSIS
# ============================================================

@app.route("/analyze-resume", methods=["POST"])
def analyze_resume():

    try:

        data = request.get_json()

        resume_text = data.get("resume_text", "")

        if not resume_text:

            return jsonify({
                "status": "error",
                "message": "Resume text is required"
            }), 400

        detected_skills = detect_skills(resume_text)

        text_lower = resume_text.lower()

        education = []

        if "b.tech" in text_lower or "btech" in text_lower:
            education.append("B.Tech")

        if "b.e" in text_lower:
            education.append("B.E")

        if "m.tech" in text_lower:
            education.append("M.Tech")

        if "mba" in text_lower:
            education.append("MBA")

        if "bca" in text_lower:
            education.append("BCA")

        if "mca" in text_lower:
            education.append("MCA")

        sections = []

        possible_sections = [
            "education",
            "experience",
            "projects",
            "skills",
            "internship",
            "certification",
            "certifications"
        ]

        for section in possible_sections:

            if section in text_lower:
                sections.append(section)

        profile_completeness = 100

        return jsonify({

            "status": "success",

            "skills_detected": len(detected_skills),

            "detected_skills": detected_skills,

            "education": education,

            "sections_found": sections,

            "profile_completeness": profile_completeness

        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        target_role = data.get("target_role", "")

        current_skills = data.get("current_skills", [])

        resume_text = data.get("resume_text", "")

        if not target_role:

            return jsonify({
                "status": "error",
                "message": "Target role is required"
            }), 400

        required_skills = ROLE_SKILLS.get(target_role, [])

        resume_skills = detect_skills(resume_text)

        all_current_skills = list(
            dict.fromkeys(current_skills + resume_skills)
        )

        matched_skills = [
            skill
            for skill in required_skills
            if skill in all_current_skills
        ]

        missing_skills = [
            skill
            for skill in required_skills
            if skill not in all_current_skills
        ]

        score = calculate_percentage(
            matched_skills,
            required_skills
        )

        if score >= 80:

            level = "Job Ready"

        elif score >= 60:

            level = "Good Progress"

        elif score >= 40:

            level = "Average"

        else:

            level = "Needs Improvement"

        return jsonify({

            "status": "success",

            "target_role": target_role,

            "required_skills": required_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "required_count": len(required_skills),

            "matched_count": len(matched_skills),

            "missing_count": len(missing_skills),

            "score": score,

            "level": level

        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ============================================================
# LEARNING ROADMAP
# ============================================================

@app.route("/roadmap", methods=["POST"])
def roadmap():

    try:

        data = request.get_json()

        missing_skills = data.get("missing_skills", [])

        target_role = data.get("target_role", "")

        roadmap_data = []

        for index, skill in enumerate(missing_skills):

            if index == 0:

                priority = "High"

            elif index <= 2:

                priority = "High"

            else:

                priority = "Medium"

            roadmap_data.append({

                "step": index + 1,

                "skill": skill,

                "priority": priority,

                "estimated_duration": "1-3 weeks",

                "goal": f"Learn and practice {skill} for {target_role}"

            })

        return jsonify({

            "status": "success",

            "target_role": target_role,

            "roadmap": roadmap_data

        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ============================================================
# JOB DESCRIPTION MATCHER
# ============================================================

@app.route("/job-match", methods=["POST"])
def job_match():

    try:

        data = request.get_json()

        resume_text = data.get("resume_text", "")

        job_description = data.get("job_description", "")

        if not resume_text:

            return jsonify({
                "status": "error",
                "message": "Resume text is required"
            }), 400

        if not job_description:

            return jsonify({
                "status": "error",
                "message": "Job description is required"
            }), 400

        resume_skills = detect_skills(resume_text)

        required_skills = detect_skills(job_description)

        matched_skills = [
            skill
            for skill in required_skills
            if skill in resume_skills
        ]

        missing_skills = [
            skill
            for skill in required_skills
            if skill not in resume_skills
        ]

        match_percentage = calculate_percentage(
            matched_skills,
            required_skills
        )

        if match_percentage >= 80:

            match_level = "Excellent Match"

        elif match_percentage >= 60:

            match_level = "Good Match"

        elif match_percentage >= 40:

            match_level = "Partial Match"

        else:

            match_level = "Low Match"

        return jsonify({

            "status": "job_match_completed",

            "resume_skills": resume_skills,

            "required_skills": required_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "required_count": len(required_skills),

            "matched_count": len(matched_skills),

            "missing_count": len(missing_skills),

            "match_percentage": match_percentage,

            "match_level": match_level

        })

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ============================================================
# AI RECOMMENDATION ENGINE
# ============================================================

@app.route("/ai-recommendation", methods=["POST"])
def ai_recommendation():

    try:

        data = request.get_json()

        target_role = data.get("target_role", "")

        missing_skills = data.get("missing_skills", [])

        if not target_role:

            return jsonify({

                "status": "error",

                "message": "Target role is required"

            }), 400

        if not missing_skills:

            return jsonify({

                "status": "success",

                "target_role": target_role,

                "total_missing_skills": 0,

                "recommendations": [],

                "message": "No skill gaps found. You are ready for this role!"

            })

        # ----------------------------------------------------
        # Skill Priority
        # ----------------------------------------------------

        priority_order = [

            "SQL",

            "Python",

            "Excel",

            "Statistics",

            "Pandas",

            "Power BI",

            "NumPy",

            "Machine Learning",

            "Scikit-learn",

            "Data Structures",

            "Algorithms",

            "Git",

            "ETL",

            "Apache Spark",

            "Cloud",

            "HTML",

            "CSS",

            "JavaScript",

            "React",

            "Java",

            "OOP"

        ]

        ordered_skills = []

        for skill in priority_order:

            if skill in missing_skills:

                ordered_skills.append(skill)

        for skill in missing_skills:

            if skill not in ordered_skills:

                ordered_skills.append(skill)

        # ----------------------------------------------------
        # Recommendation Generation
        # ----------------------------------------------------

        recommendations = []

        for index, skill in enumerate(ordered_skills):

            if index <= 2:

                priority = "High"

                duration = "2-3 weeks"

            else:

                priority = "Medium"

                duration = "1-2 weeks"

            if skill == "SQL":

                reason = (
                    "SQL is important for querying databases, "
                    "data cleaning and data analysis."
                )

                action = (
                    "Learn SELECT, WHERE, JOIN, GROUP BY, "
                    "subqueries and window functions."
                )

            elif skill == "Excel":

                reason = (
                    "Excel is widely used for data cleaning, "
                    "analysis and reporting."
                )

                action = (
                    "Practice formulas, Pivot Tables, "
                    "lookup functions and dashboards."
                )

            elif skill == "Power BI":

                reason = (
                    "Power BI helps create interactive dashboards "
                    "and business reports."
                )

                action = (
                    "Learn Power Query, data modelling, "
                    "DAX and dashboard creation."
                )

            elif skill == "Statistics":

                reason = (
                    "Statistics helps understand data patterns "
                    "and make data-driven conclusions."
                )

                action = (
                    "Study mean, median, probability, "
                    "distribution, correlation and hypothesis testing."
                )

            elif skill == "Pandas":

                reason = (
                    "Pandas is widely used for data manipulation "
                    "and analysis in Python."
                )

                action = (
                    "Practice DataFrame operations, filtering, "
                    "grouping, merging and data cleaning."
                )

            elif skill == "Python":

                reason = (
                    "Python is a core programming language "
                    "for data analysis and automation."
                )

                action = (
                    "Practice functions, data structures, "
                    "file handling and data analysis projects."
                )

            else:

                reason = (
                    f"{skill} is relevant to the "
                    f"{target_role} role."
                )

                action = (
                    f"Learn {skill}, practice it with projects "
                    "and demonstrate it through your portfolio."
                )

            recommendations.append({

                "rank": index + 1,

                "skill": skill,

                "priority": priority,

                "estimated_time": duration,

                "reason": reason,

                "action": action

            })

        return jsonify({

            "status": "success",

            "target_role": target_role,

            "total_missing_skills": len(ordered_skills),

            "recommendations": recommendations,

            "next_step": (
                "Complete the high-priority skills first, "
                "then build practical projects."
            )

        })

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ============================================================
# COMPLETE ANALYSIS
# ============================================================

@app.route("/complete-analysis", methods=["POST"])
def complete_analysis():

    try:

        data = request.get_json()

        resume_text = data.get("resume_text", "")

        target_role = data.get("target_role", "")

        current_skills = data.get("current_skills", [])

        if not resume_text:

            return jsonify({

                "status": "error",

                "message": "Resume text is required"

            }), 400

        if not target_role:

            return jsonify({

                "status": "error",

                "message": "Target role is required"

            }), 400

        # Resume skills

        resume_skills = detect_skills(resume_text)

        # Required skills

        required_skills = ROLE_SKILLS.get(
            target_role,
            []
        )

        # All available skills

        all_skills = list(
            dict.fromkeys(
                current_skills + resume_skills
            )
        )

        # Matched skills

        matched_skills = [

            skill

            for skill in required_skills

            if skill in all_skills

        ]

        # Missing skills

        missing_skills = [

            skill

            for skill in required_skills

            if skill not in all_skills

        ]

        # Score

        score = calculate_percentage(

            matched_skills,

            required_skills

        )

        # Level

        if score >= 80:

            level = "Job Ready"

        elif score >= 60:

            level = "Good Progress"

        elif score >= 40:

            level = "Average"

        else:

            level = "Needs Improvement"

        # AI recommendations

        priority_order = [

            "SQL",
            "Python",
            "Excel",
            "Statistics",
            "Pandas",
            "Power BI",
            "NumPy",
            "Machine Learning",
            "Scikit-learn",
            "Data Structures",
            "Algorithms",
            "Git",
            "ETL",
            "Apache Spark",
            "Cloud",
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Java",
            "OOP"

        ]

        recommendations = []

        ordered_missing = []

        for skill in priority_order:

            if skill in missing_skills:

                ordered_missing.append(skill)

        for skill in missing_skills:

            if skill not in ordered_missing:

                ordered_missing.append(skill)

        for index, skill in enumerate(ordered_missing):

            priority = (
                "High"
                if index <= 2
                else "Medium"
            )

            recommendations.append({

                "rank": index + 1,

                "skill": skill,

                "priority": priority,

                "estimated_time": (
                    "2-3 weeks"
                    if priority == "High"
                    else "1-2 weeks"
                )

            })

        return jsonify({

            "status": "success",

            "target_role": target_role,

            "resume_skills": resume_skills,

            "required_skills": required_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "score": score,

            "level": level,

            "ai_recommendations": recommendations

        })

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print("AI SKILL-GAP ANALYZER BACKEND")

    print("=" * 60)

    print("Backend URL: http://127.0.0.1:5000")

    print("Status: Running")

    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )