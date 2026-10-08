# CareerLens AI — Evidence-Backed AI Career Intelligence Platform

CareerLens AI doesn't just score a resume. It explains **why** a candidate matches a job, verifies whether claims in the resume are supported by **concrete evidence**, identifies **skill gaps**, generates an actionable **personalized learning roadmap**, and conducts an **adaptive mock interview** using an AI agent loop.

---

## 🧭 User Flow

1. **Welcome** (`/`) – intro page with a *Get Started* button.
2. **Upload** (`/upload`) – choose a PDF resume and click **Analyze Resume**.
3. **Results** (`/results`) – shown automatically after analysis:
   - best-fit role and **role-fit score**, plus a ranking across 13 role families (Frontend, Backend, Sales, ...)
   - **resume quality score** and checklist
   - matched / missing core skills
   - prioritised **suggestions**
   - **companies hiring** for your top 3 roles

4. **Interview Prep** (`/interview`) – role-based practice questions (Technical, Scenario, Behavioural, plus questions built from your resume's skills and gaps). Write an answer and get feedback. Endpoints: `POST /api/interview/questions`, `POST /api/interview/evaluate`. Question bank: `ai-service/app/services/role_interview_service.py`.

Endpoints behind it: `POST /api/resumes/upload` → `POST /api/analyses/role-fit` (Spring Boot) → `POST /ai/analysis/role-fit` (FastAPI).
Scoring is rule-based (works without an OpenAI key); with a key, the summary and suggestions are rewritten by the LLM.
Role profiles live in `ai-service/app/services/role_service.py`; the company list lives in `backend/src/main/resources/vacancies.json`.

---

## 🏗️ Architecture Overview

```
                      ┌────────────────────────┐
                      │ React Frontend (Vite)  │
                      │ Port 5173              │
                      └───────────┬────────────┘
                                  │
                            REST  │ (API Gateway & User Flow)
                                  ▼
                      ┌────────────────────────┐
                      │   Spring Boot 3 (Java) │
                      │ Port 8080              │
                      └─────┬────────────┬─────┘
                            │            │
           JPA Persistence  │            │ WebClient HTTP
                            ▼            ▼
             ┌─────────────────┐    ┌──────────────────────┐
             │ PostgreSQL (DB) │    │  FastAPI (AI Core)   │
             │ Port 5432       │    │  Port 8000           │
             └─────────────────┘    └──────────┬───────────┘
                                               │
                                      Embeddings & LLM
                                               ▼
                                    ┌──────────────────────┐
                                    │      OpenAI API      │
                                    └──────────────────────┘
```

### Why Microservices?
- **Spring Boot Backend**: Handles authentication, user records, relational database integrity, file upload persistence, transaction boundaries, and business rules.
- **Python FastAPI Service**: Handles PDF parsing (PyMuPDF), LLM structured extraction (OpenAI), vector similarity (embeddings & cosine distance), and the stateful adaptive interview loop.
- **React UI**: High-performance single page application built with Vite, Material UI, Recharts, and React Router.

---

## 📂 Project Structure

```
Resume Analyzer/
├── .env.example              # Central environment variables template
├── .gitignore                # Universal gitignore (Node, Java, Python)
├── docker-compose.yml        # Orchestration for Postgres, FastAPI, Spring Boot, React
├── README.md                 # Complete system guide
│
├── ai-service/               # FastAPI AI Microservice (Python 3.11+)
│   ├── app/
│   │   ├── main.py           # FastAPI entrypoint, CORS, routers
│   │   ├── config.py         # App settings & environment loading
│   │   ├── schemas/          # Pydantic schemas (resume, job, analysis, interview)
│   │   ├── services/         # PyMuPDF, LLM, embeddings, interview agent
│   │   └── routers/          # Endpoints (/resume, /analysis, /interview)
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Container build for AI service
│
├── backend/                  # Spring Boot 3 Backend (Java 21)
│   ├── src/main/java/com/careerlens/
│   │   ├── CareerLensApplication.java
│   │   ├── entity/           # User, Resume, JobDescription, Analysis
│   │   ├── repository/       # Spring Data JPA repositories
│   │   ├── service/          # ResumeService, JobService, AnalysisService
│   │   ├── client/           # WebClient connecting to FastAPI
│   │   ├── controller/       # REST endpoints (/resumes, /jobs, /analyses, /interview, /health)
│   │   └── dto/              # Request & Response contracts
│   ├── src/main/resources/
│   │   ├── application.yml   # Multi-profile Spring configuration
│   │   ├── application-dev.yml # Local dev profile (H2 fallback & Postgres)
│   │   └── schema.sql        # Database schema definitions
│   ├── pom.xml               # Maven dependencies
│   ├── mvnw & mvnw.cmd       # Official Maven wrapper
│   └── Dockerfile            # Multi-stage container build
│
└── frontend/                 # React UI (Vite + Material UI)
    ├── src/
    │   ├── components/       # Navbar, ScoreCard, SkillMatch, EvidenceCard, GapAnalysis, ResumeUploader
    │   ├── pages/            # Dashboard, UploadResume, Analysis, Interview
    │   ├── services/api.js   # Central Axios client
    │   ├── App.jsx           # Dark theme provider & Router
    │   ├── main.jsx          # Entrypoint
    │   └── index.css         # Styling system
    ├── package.json          # Node dependencies
    ├── vite.config.js        # Vite build & backend proxy
    └── Dockerfile            # Nginx production build
```

---

## ⚡ Quick Start: Running the Services

### Option A: Run Everything via Docker Compose (Recommended)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. (Optional) Insert your `OPENAI_API_KEY` into `.env`. If not provided, the AI service automatically runs in intelligent mock/fallback mode.
3. Start all containers:
   ```bash
   docker compose up --build
   ```
4. Access the applications:
   - **Frontend UI**: [http://localhost:5173](http://localhost:5173)
   - **Spring Boot Backend**: [http://localhost:8080/api/health](http://localhost:8080/api/health)
   - **FastAPI AI Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **PostgreSQL**: Port 5432 (`careerlens` / `postgres`)

---

### Option B: Run Individually on Host (Local Development)

You can run each service directly in separate terminal tabs on Windows:

#### 1. FastAPI AI Service (Terminal 1)
```powershell
cd ai-service
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*Health check:* [http://localhost:8000/health](http://localhost:8000/health)

#### 2. Spring Boot Backend (Terminal 2)
The backend is pre-configured with a development profile (`dev`) that runs with an in-memory database fallback or connects to local PostgreSQL if available.
```powershell
cd backend
.\mvnw.cmd spring-boot:run
```
*Health check:* [http://localhost:8080/api/health](http://localhost:8080/api/health)

#### 3. React Frontend (Terminal 3)
```powershell
cd frontend
cmd /c npm install
cmd /c npm run dev
```
*Frontend URL:* [http://localhost:5173](http://localhost:5173)

---

## 📊 Transparent Multi-Factor Scoring

Unlike simplistic keyword counts, CareerLens uses a transparent scoring framework:

$$\text{Final Score} = 0.35 \times \text{Skill Match} + 0.20 \times \text{Evidence Strength} + 0.15 \times \text{Project Relevance} + 0.10 \times \text{Experience Alignment} + 0.10 \times \text{Education Alignment} + 0.10 \times \text{Resume Quality}$$

---

## 🤖 Adaptive AI Interview Loop

The interview agent is not a static list of questions. It runs an adaptive agent loop:
```
Resume + Job Description
         │
         ▼
  Generate Question ──► Candidate Answers ──► Evaluate Answer
                                                    │
                                                    ├── Strong ──► Escalate Difficulty
                                                    └── Weak   ──► Ask Targeted Follow-up
```
