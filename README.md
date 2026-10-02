\# 🎯 AI Skill-Gap Analyzer \& Personalized Learning



An AI-powered career assistance application that analyzes a user's skills, identifies skill gaps for a target career role, analyzes resume skills, matches job descriptions, and generates a personalized learning roadmap.



\## 🚀 Project Overview



The \*\*AI Skill-Gap Analyzer\*\* helps students and job seekers understand their current technical skills and identify the skills they need to develop for their desired career role.



The application combines \*\*skill-gap analysis, resume analysis, job-description matching, career readiness scoring, and personalized learning roadmaps\*\* in one platform.



\## ✨ Key Features



\### 🎯 Skill Gap Analysis



\* Compare current skills with target-role requirements.

\* Identify matched and missing skills.

\* Calculate a career-readiness score.

\* Display skill gaps using interactive visualizations.



\### 📄 Resume Skill Analysis



\* Upload a PDF resume.

\* Extract text from the resume.

\* Detect relevant technical skills automatically.

\* Compare resume skills with career requirements.



\### 💼 Job Description Matcher



\* Compare user skills with job-description requirements.

\* Calculate job-match percentage.

\* Display matched and missing skills.

\* Show the overall match level.



\### 🗺️ Personalized Learning Roadmap



\* Identify skills that need improvement.

\* Generate a structured learning roadmap.

\* Prioritize missing skills for the selected career role.



\### 📊 Interactive Dashboard



\* Career readiness progress.

\* Skill-gap metrics.

\* Interactive charts.

\* Matched and missing skill sections.



\### 🔌 Frontend + Backend Architecture



\* Streamlit-based frontend.

\* Flask-based backend.

\* REST API communication between frontend and backend.



\## 🛠️ Technologies Used



\### Frontend



\* Python

\* Streamlit

\* Pandas

\* Plotly



\### Backend



\* Python

\* Flask

\* Flask-CORS



\### Data Science / Machine Learning



\* NumPy

\* Pandas

\* Scikit-learn



\### Resume Processing



\* PyPDF



\### Development Tools



\* Git

\* GitHub

\* Visual Studio Code



\## 🏗️ Project Structure



```text

AI-Skill-Gap-Analyzer/

│

├── backend/

│   ├── app.py

│   └── app\_backup\_step3.py

│

├── frontend/

│   ├── app.py

│   └── app\_backup1.py

│

├── README.md

├── requirements.txt

├── start.py

├── .gitignore

└── LICENSE

```



\## ⚙️ Installation \& Setup



\### 1. Clone the Repository



```bash

git clone https://github.com/Anubhav-Singh47/ai-skill-gap-analyzer.git

```



\### 2. Open the Project



```bash

cd ai-skill-gap-analyzer

```



\### 3. Create a Virtual Environment



```bash

python -m venv venv

```



\### 4. Activate the Virtual Environment



For Windows:



```bash

venv\\Scripts\\activate

```



\### 5. Install Dependencies



```bash

pip install -r requirements.txt

```



\## ▶️ Running the Application



\### Start the Backend



Open a terminal and run:



```bash

python backend/app.py

```



The Flask backend runs on:



```text

http://127.0.0.1:5000

```



\### Start the Frontend



Open another terminal and run:



```bash

python -m streamlit run frontend/app.py

```



The Streamlit application will open in your browser.



Default URL:



```text

http://localhost:8501

```



\## 🔄 Application Workflow



```text

User

&#x20; ↓

Enter Profile Information

&#x20; ↓

Select Target Career Role

&#x20; ↓

Upload Resume / Select Skills

&#x20; ↓

Resume \& Skill Analysis

&#x20; ↓

Compare Required Skills

&#x20; ↓

Identify Skill Gaps

&#x20; ↓

Calculate Career Readiness

&#x20; ↓

Generate Learning Roadmap

&#x20; ↓

Job Description Matching

```



\## 🎯 Supported Career Roles



The application currently supports analysis for:



\* Data Analyst

\* Data Scientist

\* Software Developer

\* Data Engineer

\* Web Developer



Each role has a defined set of technical skills that are used for skill-gap analysis.



\## 📊 Example Analysis



\### Matched Skills



```text

✓ Python

✓ Pandas

✓ SQL

```



\### Missing Skills



```text

⚠ Power BI

⚠ Statistics

⚠ Excel

```



The missing skills are then used to create a personalized learning roadmap.



\## 🔐 Privacy



Resume files are processed for skill extraction and analysis. Users should avoid uploading unnecessary sensitive personal information.



\## 🔮 Future Enhancements



\* 🤖 Advanced AI-based skill extraction

\* 🧠 NLP-based resume understanding

\* 🔎 Real-time job recommendations

\* 🌐 Job portal integration

\* 📚 Course recommendations

\* 📈 Skill-demand analytics

\* ☁️ Cloud deployment

\* 🔐 User authentication

\* 🗄️ Database integration

\* 📊 Advanced career analytics



\## 👨‍💻 Author



\*\*Anubhav Singh\*\*



B.Tech Computer Science \& Engineering



\### GitHub



https://github.com/Anubhav-Singh47



\## 📄 License



This project is licensed under the MIT License.



