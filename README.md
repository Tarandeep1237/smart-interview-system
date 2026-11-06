# AI-Based Smart Interview Evaluation System

An AI-powered web application that helps candidates prepare for technical interviews through resume-based skill extraction, personalized interview question generation, automated answer evaluation, and performance reporting.

## 1. Project Overview

The AI-Based Smart Interview Evaluation System is designed to make technical interview preparation more personalized, structured, and accessible.

The system analyzes uploaded resumes, extracts relevant technical skills, generates interview questions based on candidate skills, evaluates submitted answers using AI, and presents interview performance through evaluation results and reports.

## 2. Key Features

- **User Authentication:** Candidate registration, login, and logout.
- **Profile Management:** Manage candidate profile information.
- **Resume Upload:** Upload resumes in PDF and DOCX formats.
- **Resume Parsing:** Extract text and relevant information from uploaded resumes.
- **Skill Extraction:** Identify technical skills from resume content.
- **AI-Based Question Generation:** Generate personalized technical interview questions.
- **Answer Evaluation:** Evaluate candidate answers using AI.
- **Performance Analysis:** Calculate and present interview evaluation scores.
- **Interview Results:** Display interview performance and evaluation feedback.
- **Report Generation:** Generate interview evaluation reports.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | MySQL |
| AI Integration | OpenAI API |
| Database Connectivity | mysql-connector-python |
| PDF Processing | PyPDF |
| DOCX Processing | python-docx |
| Environment Configuration | python-dotenv |

## 4. Project Architecture

The application follows a modular architecture that separates routing, business logic, AI integration, database operations, and frontend components.

```text
Interview-System/
│
├── backend/
│   ├── ai/
│   │   ├── answer_evaluator.py
│   │   ├── openai_client.py
│   │   ├── question_generator.py
│   │   └── skill_extractor.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── schema.sql
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── dashboard_routes.py
│   │   ├── interview_routes.py
│   │   ├── main_routes.py
│   │   ├── profile_routes.py
│   │   ├── results_routes.py
│   │   ├── resume_routes.py
│   │   └── skill_routes.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── dashboard_service.py
│   │   ├── evaluation_service.py
│   │   ├── interview_service.py
│   │   ├── profile_service.py
│   │   ├── report_service.py
│   │   ├── results_service.py
│   │   ├── resume_parser.py
│   │   ├── resume_service.py
│   │   └── skill_service.py
│   │
│   ├── config.py
│   └── __init__.py
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── dashboard.js
│   │       ├── interview.js
│   │       ├── interview_setup.js
│   │       ├── login.js
│   │       ├── profile.js
│   │       ├── register.js
│   │       ├── results.js
│   │       └── resume.js
│   │
│   └── templates/
│       ├── dashboard.html
│       ├── index.html
│       ├── interview.html
│       ├── interview_setup.html
│       ├── login.html
│       ├── navbar.html
│       ├── profile.html
│       ├── register.html
│       └── resume.html
│
├── docs/
├── reports/
├── tests/
├── uploads/
│
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

## 5. Application Workflow

1. Candidate registers and logs into the application.
2. Candidate completes their profile.
3. Candidate uploads a resume.
4. The system extracts text from the uploaded resume.
5. Technical skills are identified from the extracted content.
6. Personalized interview questions are generated using AI.
7. Candidate submits answers to the generated questions.
8. The AI evaluation component evaluates the submitted answers.
9. Evaluation scores and feedback are generated.
10. Interview results and performance reports are presented to the candidate.

## 6. Database Design

The application uses MySQL to store candidate information, interview data, responses, and evaluation results.

The database is named:

`smart_interview_db`

The database contains the following tables:

| Table | Purpose |
|---|---|
| users | Stores candidate account information |
| profiles | Stores candidate profile details |
| resumes | Stores resume records and extracted text |
| interviews | Stores interview session information |
| questions | Stores generated interview questions |
| responses | Stores candidate answers |
| evaluations | Stores answer evaluation scores and feedback |
| interview_reports | Stores overall interview reports |

The database schema is available in:

`backend/database/schema.sql`

## 7. Installation and Setup

### Prerequisites

- Python 3.10 or later
- MySQL Server
- OpenAI API key
- Git

### Step 1: Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Interview-System
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root directory.

Add the following configuration:

```env
FLASK_SECRET_KEY=your_flask_secret_key

DB_HOST=localhost
DB_PORT=3306
DB_NAME=smart_interview_db
DB_USER=your_database_username
DB_PASSWORD=your_database_password

OPENAI_API_KEY=your_openai_api_key
```

Replace the example values with your actual local configuration.

**Important:** Never upload your `.env` file or expose API keys, passwords, or secret keys publicly.

### Step 5: Configure the MySQL Database

1. Start your MySQL server.
2. Create the database:

```sql
CREATE DATABASE smart_interview_db;
```

3. Execute the SQL statements in `backend/database/schema.sql`.
4. Ensure that the database credentials in `.env` match your MySQL configuration.

### Step 6: Run the Application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## 8. Security Considerations

- Environment variables are used to manage sensitive configuration.
- `.env` files are excluded from Git tracking.
- Virtual environments and Python cache files are excluded from version control.
- Uploaded resumes and personal data are excluded from the public repository.
- Flask session security is configured using an environment-based secret key.

## 9. Future Enhancements

- Advanced interview performance analytics.
- Additional interview categories and difficulty levels.
- Enhanced evaluation metrics.
- Expanded interview preparation features.

## 10. Author

**Tarandeep Singh**

AI/ML Engineering Student

---

*Developed as an AI/ML engineering project to support personalized technical interview preparation and automated interview evaluation.*