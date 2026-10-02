from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# ============================================================
# ROLE SKILLS
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
# LEARNING RESOURCES
# ============================================================

LEARNING_RESOURCES = {

    "Python": {
        "level": "Beginner to Intermediate",
        "duration": "2-3 weeks",
        "topics": [
            "Python basics",
            "Variables and data types",
            "Conditions and loops",
            "Functions",
            "Lists and dictionaries",
            "File handling",
            "Object Oriented Programming"
        ]
    },

    "SQL": {
        "level": "Beginner to Intermediate",
        "duration": "2 weeks",
        "topics": [
            "SELECT",
            "WHERE",
            "GROUP BY",
            "ORDER BY",
            "JOIN",
            "Subqueries",
            "Aggregate functions"
        ]
    },

    "Excel": {
        "level": "Beginner to Intermediate",
        "duration": "1-2 weeks",
        "topics": [
            "Formulas",
            "Functions",
            "VLOOKUP/XLOOKUP",
            "Pivot Tables",
            "Charts",
            "Data Cleaning"
        ]
    },

    "Power BI": {
        "level": "Beginner",
        "duration": "2 weeks",
        "topics": [
            "Power BI interface",
            "Data import",
            "Data cleaning",
            "Data modelling",
            "DAX basics",
            "Dashboard creation"
        ]
    },

    "Statistics": {
        "level": "Intermediate",
        "duration": "2 weeks",
        "topics": [
            "Mean",
            "Median",
            "Mode",
            "Variance",
            "Standard deviation",
            "Probability",
            "Correlation"
        ]
    },

    "Pandas": {
        "level": "Intermediate",
        "duration": "1 week",
        "topics": [
            "Series",
            "DataFrame",
            "Filtering",
            "Sorting",
            "Missing values",
            "GroupBy",
            "Data analysis"
        ]
    },

    "NumPy": {
        "level": "Intermediate",
        "duration": "1 week",
        "topics": [
            "Arrays",
            "Array operations",
            "Indexing",
            "Slicing",
            "Mathematical operations"
        ]
    },

    "Machine Learning": {
        "level": "Intermediate",
        "duration": "3-4 weeks",
        "topics": [
            "Supervised learning",
            "Unsupervised learning",
            "Regression",
            "Classification",
            "Clustering",
            "Model evaluation"
        ]
    },

    "Scikit-learn": {
        "level": "Intermediate",
        "duration": "2 weeks",
        "topics": [
            "Data preprocessing",
            "Train-test split",
            "Regression",
            "Classification",
            "Model evaluation"
        ]
    },

    "Java": {
        "level": "Beginner to Intermediate",
        "duration": "3 weeks",
        "topics": [
            "Java basics",
            "Classes and objects",
            "Inheritance",
            "Polymorphism",
            "Exception handling",
            "Collections"
        ]
    },

    "Data Structures": {
        "level": "Intermediate",
        "duration": "3 weeks",
        "topics": [
            "Arrays",
            "Linked Lists",
            "Stacks",
            "Queues",
            "Trees",
            "Hashing"
        ]
    },

    "Algorithms": {
        "level": "Intermediate",
        "duration": "3 weeks",
        "topics": [
            "Searching",
            "Sorting",
            "Recursion",
            "Greedy algorithms",
            "Dynamic programming"
        ]
    },

    "Git": {
        "level": "Beginner",
        "duration": "3-5 days",
        "topics": [
            "Git basics",
            "Repositories",
            "Commit",
            "Branch",
            "Merge",
            "GitHub"
        ]
    },

    "OOP": {
        "level": "Intermediate",
        "duration": "1 week",
        "topics": [
            "Classes",
            "Objects",
            "Inheritance",
            "Encapsulation",
            "Polymorphism",
            "Abstraction"
        ]
    },

    "ETL": {
        "level": "Intermediate",
        "duration": "2 weeks",
        "topics": [
            "Extract",
            "Transform",
            "Load",
            "Data pipelines",
            "Data cleaning"
        ]
    },

    "Apache Spark": {
        "level": "Intermediate",
        "duration": "2-3 weeks",
        "topics": [
            "Spark basics",
            "RDD",
            "DataFrames",
            "Spark SQL",
            "Distributed processing"
        ]
    },

    "Cloud": {
        "level": "Beginner",
        "duration": "2-3 weeks",
        "topics": [
            "Cloud basics",
            "AWS/Azure basics",
            "Storage",
            "Compute",
            "Databases"
        ]
    },

    "HTML": {
        "level": "Beginner",
        "duration": "4-5 days",
        "topics": [
            "HTML structure",
            "Forms",
            "Tables",
            "Semantic HTML"
        ]
    },

    "CSS": {
        "level": "Beginner",
        "duration": "1 week",
        "topics": [
            "Selectors",
            "Box model",
            "Flexbox",
            "Grid",
            "Responsive design"
        ]
    },

    "JavaScript": {
        "level": "Beginner to Intermediate",
        "duration": "2-3 weeks",
        "topics": [
            "Variables",
            "Functions",
            "Arrays",
            "Objects",
            "DOM",
            "Events",
            "Async JavaScript"
        ]
    },

    "React": {
        "level": "Intermediate",
        "duration": "2-3 weeks",
        "topics": [
            "Components",
            "Props",
            "State",
            "Hooks",
            "API integration"
        ]
    }
}


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {
    "python": "Python",
    "python3": "Python",

    "sql": "SQL",
    "mysql": "SQL",
    "postgresql": "SQL",
    "postgres": "SQL",
    "database": "SQL",

    "excel": "Excel",
    "microsoft excel": "Excel",

    "power bi": "Power BI",
    "powerbi": "Power BI",

    "statistics": "Statistics",
    "statistical analysis": "Statistics",

    "pandas": "Pandas",
    "numpy": "NumPy",

    "machine learning": "Machine Learning",
    "machine-learning": "Machine Learning",
    "ml": "Machine Learning",

    "scikit-learn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",

    "java": "Java",

    "data structures": "Data Structures",
    "data structure": "Data Structures",
    "dsa": "Data Structures",

    "algorithms": "Algorithms",
    "algorithm": "Algorithms",

    "git": "Git",
    "github": "Git",
    "gitlab": "Git",

    "object oriented programming": "OOP",
    "object-oriented programming": "OOP",
    "oop": "OOP",

    "etl": "ETL",

    "apache spark": "Apache Spark",
    "spark": "Apache Spark",

    "cloud": "Cloud",
    "cloud computing": "Cloud",

    "html": "HTML",
    "html5": "HTML",

    "css": "CSS",
    "css3": "CSS",

    "javascript": "JavaScript",
    "java script": "JavaScript",
    "js": "JavaScript",

    "react": "React",
    "reactjs": "React"
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_skill(skill):

    if not skill:
        return None

    skill = str(skill).strip()
    lower_skill = skill.lower()

    if lower_skill in SKILL_ALIASES:
        return SKILL_ALIASES[lower_skill]

    for alias, standard_name in SKILL_ALIASES.items():
        if alias in lower_skill:
            return standard_name

    return skill


def normalize_skill_list(skills):

    if not skills:
        return []

    normalized = []

    for skill in skills:

        standard_skill = normalize_skill(skill)

        if standard_skill and standard_skill not in normalized:
            normalized.append(standard_skill)

    return normalized


def extract_skills_from_text(text):

    if not text:
        return []

    text_lower = text.lower()

    detected_skills = []

    for alias, standard_name in SKILL_ALIASES.items():

        if alias in text_lower:

            if standard_name not in detected_skills:
                detected_skills.append(standard_name)

    return detected_skills


def calculate_skill_gap(current_skills, required_skills):

    current_skills = normalize_skill_list(current_skills)
    required_skills = normalize_skill_list(required_skills)

    matched = []
    missing = []

    for skill in required_skills:

        if skill in current_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    total_required = len(required_skills)

    if total_required == 0:
        score = 0
    else:
        score = round(
            (len(matched) / total_required) * 100
        )

    return {
        "required": required_skills,
        "matched": matched,
        "missing": missing,
        "score": score
    }


def get_level(score):

    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Intermediate"
    else:
        return "Needs Improvement"


def generate_roadmap(missing_skills):

    roadmap = []

    for index, skill in enumerate(missing_skills, start=1):

        resource = LEARNING_RESOURCES.get(
            skill,
            {
                "level": "Beginner",
                "duration": "1-2 weeks",
                "topics": [
                    f"Learn {skill} fundamentals",
                    f"Practice {skill}",
                    f"Build a project using {skill}"
                ]
            }
        )

        roadmap.append({
            "step": index,
            "skill": skill,
            "level": resource["level"],
            "duration": resource["duration"],
            "topics": resource["topics"],
            "action": f"Learn {skill}, practice regularly and build a small project."
        })

    return roadmap


# ============================================================
# HOME
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "success",
        "message": "AI Skill-Gap Analyzer Backend is Running",
        "version": "2.0",
        "available_endpoints": [
            "/",
            "/analyze",
            "/analyze-resume",
            "/roadmap",
            "/role-recommendations",
            "/complete-analysis",
            "/ai-recommendation",
            "/job-match"
        ]
    })


# ============================================================
# ANALYZE SKILL GAP
# ============================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json(silent=True) or {}

        target_role = data.get("target_role", "")

        # IMPORTANT:
        # Frontend sends "skills", not "current_skills"
        current_skills = data.get(
            "skills",
            data.get("current_skills", [])
        )

        current_skills = normalize_skill_list(
            current_skills
        )

        if not target_role:

            return jsonify({
                "status": "error",
                "error": "target_role is required"
            }), 400

        if target_role not in ROLE_SKILLS:

            return jsonify({
                "status": "error",
                "error": "Invalid target role",
                "available_roles": list(ROLE_SKILLS.keys())
            }), 400

        required_skills = ROLE_SKILLS[target_role]

        result = calculate_skill_gap(
            current_skills,
            required_skills
        )

        score = result["score"]

        return jsonify({

            "status": "success",

            "target_role": target_role,

            "current_skills": current_skills,

            "required_skills": result["required"],

            "matched_skills": result["matched"],

            "missing_skills": result["missing"],

            # Frontend dashboard keys
            "required_count": len(result["required"]),
            "matched_count": len(result["matched"]),
            "missing_count": len(result["missing"]),

            "score": score,

            "level": get_level(score),

            # Extra compatibility keys
            "total_required": len(result["required"]),
            "total_matched": len(result["matched"]),
            "total_missing": len(result["missing"]),
            "skill_gap_score": score,
            "career_readiness": score,

            "roadmap": generate_roadmap(
                result["missing"]
            )
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


# ============================================================
# ANALYZE RESUME
# ============================================================

@app.route("/analyze-resume", methods=["POST"])
def analyze_resume():

    try:

        data = request.get_json(silent=True) or {}

        resume_text = data.get(
            "resume_text",
            ""
        )

        if not resume_text:

            return jsonify({
                "status": "error",
                "error": "resume_text is required"
            }), 400

        resume_skills = extract_skills_from_text(
            resume_text
        )

        return jsonify({

            "status": "resume_analysis_completed",

            "resume_skills": resume_skills,

            "total_skills": len(resume_skills)
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


# ============================================================
# ROADMAP
# ============================================================

@app.route("/roadmap", methods=["POST"])
def roadmap():

    try:

        data = request.get_json(silent=True) or {}

        missing_skills = data.get(
            "missing_skills",
            []
        )

        missing_skills = normalize_skill_list(
            missing_skills
        )

        roadmap_data = generate_roadmap(
            missing_skills
        )

        return jsonify({

            "status": "roadmap_generated",

            "missing_skills": missing_skills,

            "roadmap": roadmap_data,

            "learning_roadmap": roadmap_data
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


# ============================================================
# ROLE RECOMMENDATIONS
# ============================================================

@app.route("/role-recommendations", methods=["POST"])
def role_recommendations():

    try:

        data = request.get_json(silent=True) or {}

        resume_skills = data.get(
            "resume_skills",
            []
        )

        resume_text = data.get(
            "resume_text",
            ""
        )

        if not resume_skills and resume_text:

            resume_skills = extract_skills_from_text(
                resume_text
            )

        resume_skills = normalize_skill_list(
            resume_skills
        )

        recommendations = []

        for role, required_skills in ROLE_SKILLS.items():

            result = calculate_skill_gap(
                resume_skills,
                required_skills
            )

            recommendations.append({

                "role": role,

                "score": result["score"],

                "matched_skills": result["matched"],

                "missing_skills": result["missing"],

                "required_skills": result["required"]
            })

        recommendations.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return jsonify({

            "status": "role_recommendation_completed",

            "resume_skills": resume_skills,

            "recommendations": recommendations
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


# ============================================================
# AI RECOMMENDATION
# ============================================================

@app.route("/ai-recommendation", methods=["POST"])
def ai_recommendation():

    try:

        data = request.get_json(silent=True) or {}

        target_role = data.get(
            "target_role",
            ""
        )

        missing_skills = data.get(
            "missing_skills",
            []
        )

        missing_skills = normalize_skill_list(
            missing_skills
        )

        recommendations = []

        for skill in missing_skills:

            resource = LEARNING_RESOURCES.get(
                skill,
                {
                    "level": "Beginner",
                    "duration": "1-2 weeks",
                    "topics": []
                }
            )

            if skill in [
                "Python",
                "SQL",
                "Statistics",
                "Data Structures",
                "Algorithms"
            ]:
                priority = "High"
            else:
                priority = "Medium"

            recommendations.append({

                "skill": skill,

                "priority": priority,

                "estimated_time": resource["duration"],

                "reason": (
                    f"{skill} is a required skill for "
                    f"the {target_role} role and is currently "
                    f"missing from your skill profile."
                ),

                "action": (
                    f"Study {skill} fundamentals, "
                    f"practice real-world problems and "
                    f"build a project using {skill}."
                )
            })

        return jsonify({

            "status": "ai_recommendation_completed",

            "target_role": target_role,

            "recommendations": recommendations
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


# ============================================================
# JOB DESCRIPTION MATCH
# ============================================================

@app.route("/job-match", methods=["POST"])
def job_match():

    try:

        data = request.get_json(silent=True) or {}

        resume_text = data.get(
            "resume_text",
            ""
        )

        job_description = data.get(
            "job_description",
            ""
        )

        if not resume_text:

            return jsonify({
                "status": "error",
                "error": "resume_text is required"
            }), 400

        if not job_description:

            return jsonify({
                "status": "error",
                "error": "job_description is required"
            }), 400

        resume_skills = extract_skills_from_text(
            resume_text
        )

        job_skills = extract_skills_from_text(
            job_description
        )

        matched_skills = [
            skill
            for skill in job_skills
            if skill in resume_skills
        ]

        missing_skills = [
            skill
            for skill in job_skills
            if skill not in resume_skills
        ]

        total_job_skills = len(job_skills)

        if total_job_skills == 0:

            match_percentage = 0

        else:

            match_percentage = round(
                (
                    len(matched_skills)
                    / total_job_skills
                ) * 100
            )

        if match_percentage >= 80:
            match_level = "High Match"

        elif match_percentage >= 50:
            match_level = "Moderate Match"

        else:
            match_level = "Low Match"

        return jsonify({

            "status": "job_match_completed",

            "resume_skills": resume_skills,

            "job_skills": job_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "match_percentage": match_percentage,

            "match_level": match_level
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


# ============================================================
# COMPLETE ANALYSIS
# ============================================================

@app.route("/complete-analysis", methods=["POST"])
def complete_analysis():

    try:

        data = request.get_json(silent=True) or {}

        resume_text = data.get(
            "resume_text",
            ""
        )

        current_skills = data.get(
            "current_skills",
            data.get("skills", [])
        )

        target_role = data.get(
            "target_role",
            ""
        )

        resume_skills = []

        if resume_text:

            resume_skills = extract_skills_from_text(
                resume_text
            )

        combined_skills = normalize_skill_list(
            resume_skills + current_skills
        )

        target_analysis = None
        target_roadmap = []

        if target_role:

            if target_role not in ROLE_SKILLS:

                return jsonify({
                    "status": "error",
                    "error": "Invalid target role"
                }), 400

            required_skills = ROLE_SKILLS[target_role]

            result = calculate_skill_gap(
                combined_skills,
                required_skills
            )

            target_analysis = {

                "role": target_role,

                "score": result["score"],

                "matched_skills": result["matched"],

                "missing_skills": result["missing"],

                "required_skills": result["required"]
            }

            target_roadmap = generate_roadmap(
                result["missing"]
            )

        recommendations = []

        for role, required_skills in ROLE_SKILLS.items():

            result = calculate_skill_gap(
                combined_skills,
                required_skills
            )

            recommendations.append({

                "role": role,

                "score": result["score"],

                "matched_skills": result["matched"],

                "missing_skills": result["missing"],

                "required_skills": result["required"]
            })

        recommendations.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return jsonify({

            "status": "complete_analysis_completed",

            "resume_skills": resume_skills,

            "combined_skills": combined_skills,

            "target_role": target_role,

            "target_analysis": target_analysis,

            "personalized_roadmap": target_roadmap,

            "role_recommendations": recommendations
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("")
    print("===================================================")
    print(" AI SKILL-GAP ANALYZER BACKEND")
    print("===================================================")
    print("Server: http://127.0.0.1:5000")
    print("Status: RUNNING")
    print("===================================================")
    print("")

    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)