<div align="center">

# 🎯 ResumeMatch AI

### AI-Powered Resume Parsing & Job Matching Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js_14-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL_16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Gemini](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)

**Upload your resume → AI extracts your skills → Get ranked job matches instantly**

[Live Demo](#) · [Architecture](#architecture) · [Quick Start](#-quick-start) · [API Docs](#-api-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Resume Parsing Pipeline](#-resume-parsing-pipeline)
- [3-Layer Matching Engine](#-3-layer-matching-engine)
- [Frontend Pages](#-frontend-pages)
- [Environment Variables](#-environment-variables)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

ResumeMatch AI is a full-stack, production-ready platform that automates resume parsing and job matching using a 3-layer AI recommendation engine. It combines **NLP-driven skill extraction** (via Google Gemini), **semantic embeddings** (sentence-transformers), and **behavioral personalization** to deliver highly relevant job recommendations.

### The Problem
Job seekers spend 10+ hours/week manually tailoring resumes and searching job boards. Recruiters review hundreds of mismatched applications. Both sides lose.

### The Solution
Upload a resume once → AI extracts skills, experience, and keywords → A 3-layer matching engine scores and ranks every job listing → Users see only the most relevant opportunities with actionable skill gap analysis.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **AI Resume Parsing** | PDF/DOCX extraction → section detection → LLM structured parsing → skill normalization |
| 🎯 **3-Layer Matching** | Keyword (Jaccard) + Semantic (embeddings) + Personalization (behavioral signals) |
| 📊 **Match Score** | 0-100 composite score with explainable "why you match" reasons |
| 🔍 **Skill Gap Analysis** | Identifies missing skills across top job matches with frequency data |
| 🔐 **JWT Authentication** | Access + refresh token flow with Redis blacklist for logout |
| 📡 **Real-time Parsing** | Server-Sent Events (SSE) for live parsing progress updates |
| 🗃️ **S3 Storage** | MinIO (S3-compatible) for resume file storage |
| ⚡ **Async Everything** | Full async/await stack — FastAPI + SQLAlchemy async + asyncpg |
| 🧪 **Production Ready** | Docker Compose, Alembic migrations, structured logging, health checks |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js 14)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Landing  │  │ Job Feed │  │ Profile  │  │   Dashboard   │  │
│  │ + Upload │  │ + Detail │  │ + Confirm│  │   + Stats     │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬────────┘  │
│       └──────── API Client (lib/api.ts) ───────────┘           │
│                     │  JWT Auth Context                         │
└─────────────────────┼───────────────────────────────────────────┘
                      │ HTTP/SSE
┌─────────────────────┼───────────────────────────────────────────┐
│                  BACKEND (FastAPI)                               │
│  ┌──────────────────┼──────────────────────────────────────┐    │
│  │              API Routers (v1)                            │    │
│  │  /auth  /resume  /jobs  /profile  /dashboard             │    │
│  └──────────────────┼──────────────────────────────────────┘    │
│  ┌──────────────────┼──────────────────────────────────────┐    │
│  │            Service Layer (Business Logic)                │    │
│  │  auth_service  resume_service  job_service               │    │
│  │  user_service  match_service   dashboard_service         │    │
│  └──────────────────┼──────────────────────────────────────┘    │
│  ┌──────────┐  ┌────┴─────┐  ┌──────────────────────────┐      │
│  │ Parsing  │  │ Matching │  │      Data Layer          │      │
│  │ Pipeline │  │ Engine   │  │  SQLAlchemy ORM Models   │      │
│  │ • Extract│  │ •Keyword │  │  • User    • Job         │      │
│  │ • Section│  │ •Semantic│  │  • Resume  • Application │      │
│  │ • LLM    │  │ •Personal│  │  • Interaction • SavedJob│      │
│  │ • Skills │  │ •Ranker  │  │                          │      │
│  └──────────┘  └──────────┘  └──────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
        │              │              │              │
   ┌────┴────┐   ┌─────┴────┐  ┌─────┴────┐  ┌─────┴────┐
   │ MinIO   │   │PostgreSQL│  │  Redis   │  │ Gemini   │
   │ (S3)    │   │ +pgvector│  │  Cache   │  │ API      │
   └─────────┘   └──────────┘  └──────────┘  └──────────┘
```

---

## 🛠 Tech Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Async web framework with auto-generated OpenAPI docs |
| **SQLAlchemy 2.0** | Async ORM with PostgreSQL |
| **PostgreSQL 16** | Primary database with pgvector + pg_trgm extensions |
| **Redis** | Caching layer + JWT blacklist |
| **MinIO** | S3-compatible object storage for resumes |
| **Google Gemini** | LLM-powered structured resume extraction |
| **sentence-transformers** | Semantic embeddings (all-MiniLM-L6-v2) |
| **Alembic** | Database migrations |

### Frontend
| Technology | Purpose |
|-----------|---------|
| **Next.js 14** | React framework (App Router) |
| **TypeScript** | Type safety |
| **Tailwind CSS** | Utility-first styling |
| **Lucide React** | Icon library |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **Docker & Docker Compose**
- **Google Gemini API Key** ([get one free](https://ai.google.dev))

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ResumeMatch-AI.git
cd ResumeMatch-AI
```

### 2. Start infrastructure services
```bash
docker-compose up -d postgres redis minio
```

### 3. Set up the backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi[standard] uvicorn[standard] sqlalchemy[asyncio] asyncpg alembic \
    pydantic-settings "python-jose[cryptography]" "passlib[bcrypt]" python-multipart \
    redis boto3 pymupdf python-docx google-generativeai httpx numpy

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start the backend
uvicorn app.main:app --reload --port 8000
```

### 4. Seed job data
```bash
# In another terminal (with venv activated)
cd backend
python -m scripts.seed_jobs
```

### 5. Set up the frontend
```bash
cd frontend
npm install
npm run dev
```

### 6. Open the app
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📁 Project Structure

```
ResumeMatch-AI/
├── docker-compose.yml          # PostgreSQL, Redis, MinIO services
│
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── main.py             # FastAPI entrypoint
│   │   ├── config.py           # Environment configuration
│   │   ├── database.py         # SQLAlchemy async engine
│   │   ├── dependencies.py     # Shared auth/DB dependencies
│   │   │
│   │   ├── models/             # SQLAlchemy ORM models
│   │   │   ├── user.py         # User model (auth + profile)
│   │   │   ├── resume.py       # ParsedResume (skills, parsed_data)
│   │   │   ├── job.py          # Job listings + embeddings
│   │   │   ├── application.py  # Application tracking
│   │   │   └── interaction.py  # UserInteraction + SavedJob
│   │   │
│   │   ├── schemas/            # Pydantic request/response models
│   │   │   ├── auth.py         # Login, register, token
│   │   │   ├── user.py         # Profile response (matches frontend)
│   │   │   ├── resume.py       # Upload, parsed data, SSE events
│   │   │   ├── job.py          # JobMatch, JobDetail (matches frontend)
│   │   │   └── dashboard.py    # Stats, activity (matches frontend)
│   │   │
│   │   ├── routers/            # FastAPI route handlers
│   │   │   ├── auth.py         # /api/v1/auth/*
│   │   │   ├── resume.py       # /api/v1/resume/* (incl. SSE)
│   │   │   ├── jobs.py         # /api/v1/jobs/*
│   │   │   ├── profile.py      # /api/v1/profile/*
│   │   │   └── dashboard.py    # /api/v1/dashboard/*
│   │   │
│   │   ├── services/           # Business logic layer
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── resume_service.py
│   │   │   ├── job_service.py
│   │   │   ├── match_service.py
│   │   │   └── dashboard_service.py
│   │   │
│   │   ├── parsing/            # Resume parsing pipeline
│   │   │   ├── extractor.py    # PDF/DOCX text extraction
│   │   │   ├── section_detector.py # Header-based section splitting
│   │   │   ├── llm_parser.py   # Gemini structured extraction
│   │   │   ├── skill_normalizer.py # 500+ skill alias mapping
│   │   │   └── pipeline.py     # Orchestrator with SSE progress
│   │   │
│   │   ├── matching/           # 3-layer recommendation engine
│   │   │   ├── keyword_matcher.py  # Jaccard skill overlap
│   │   │   ├── semantic_matcher.py # Embedding cosine similarity
│   │   │   ├── personalizer.py     # Behavioral signals + decay
│   │   │   └── ranker.py          # Weighted final score
│   │   │
│   │   └── utils/              # Shared utilities
│   │       ├── security.py     # JWT + bcrypt
│   │       ├── storage.py      # S3/MinIO operations
│   │       └── cache.py        # Redis helpers
│   │
│   ├── scripts/
│   │   └── seed_jobs.py        # Seeds ~100 realistic job listings
│   ├── alembic/                # Database migrations
│   ├── tests/                  # Pytest test suite
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   # Next.js 14 frontend
│   ├── src/
│   │   ├── app/                # Next.js App Router pages
│   │   │   ├── page.tsx        # Landing + auth + upload
│   │   │   ├── parsing/        # Real-time parsing progress (SSE)
│   │   │   ├── jobs/           # Job feed + detail pages
│   │   │   ├── profile/        # Profile view + confirm parsed data
│   │   │   └── dashboard/      # Stats + activity feed
│   │   │
│   │   ├── components/shared/  # Reusable UI components
│   │   ├── contexts/           # AuthContext (JWT state management)
│   │   ├── hooks/              # useJobFeed, useResumeParsing, useDashboard
│   │   ├── lib/api.ts          # Typed API client (all backend endpoints)
│   │   └── data/mockData.ts    # Fallback mock data (legacy)
│   │
│   ├── next.config.ts          # API proxy rewrites
│   └── .env.local
│
└── ResumeMatch_AI_Blueprint/   # Architecture documentation
```

---

## 📡 API Documentation

Once the backend is running, full interactive docs are at **http://localhost:8000/docs**

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Create account |
| `POST` | `/api/v1/auth/login` | Get JWT tokens |
| `POST` | `/api/v1/auth/refresh` | Refresh access token |
| `GET` | `/api/v1/auth/me` | Current user info |
| `POST` | `/api/v1/resume/upload` | Upload PDF/DOCX resume |
| `GET` | `/api/v1/resume` | Get parsed resume |
| `GET` | `/api/v1/resume/parsing-status` | SSE parsing progress |
| `GET` | `/api/v1/jobs/feed` | Personalized job feed |
| `GET` | `/api/v1/jobs/search?q=` | Full-text search |
| `GET` | `/api/v1/jobs/{id}` | Job detail + match analysis |
| `POST` | `/api/v1/jobs/{id}/save` | Bookmark job |
| `POST` | `/api/v1/jobs/{id}/apply` | Track application |
| `POST` | `/api/v1/jobs/{id}/dismiss` | Hide from feed |
| `GET` | `/api/v1/profile` | Full profile |
| `PUT` | `/api/v1/profile` | Update profile |
| `GET` | `/api/v1/profile/skill-gaps` | Skill gap analysis |
| `GET` | `/api/v1/dashboard/stats` | Dashboard metrics |
| `GET` | `/api/v1/dashboard/applications` | Application tracker |

---

## 🧠 Resume Parsing Pipeline

The 5-step pipeline transforms a raw PDF/DOCX into structured, normalized data:

```
Upload (PDF/DOCX) 
  → Step 1: Text Extraction (PyMuPDF / python-docx)
  → Step 2: Section Detection (regex header matching)
  → Step 3: LLM Structured Extraction (Gemini 2.0 Flash)
  → Step 4: Skill Normalization (500+ alias mappings)
  → Step 5: Metadata Computation (experience years, confidence)
  → Database Storage
```

Each step emits **Server-Sent Events** so the frontend can display real-time progress.

---

## 🏗 3-Layer Matching Engine

From `04_recommendation_engine.md`:

```
Final Score = 0.35 × Keyword + 0.45 × Semantic + 0.20 × Personalization
```

| Layer | Weight | Method | Speed |
|-------|--------|--------|-------|
| **Keyword** | 35% | Jaccard similarity on normalized skills + experience level fit | < 1ms |
| **Semantic** | 45% | Cosine similarity on sentence-transformer embeddings (384-dim) | ~10ms |
| **Personalization** | 20% | Time-decayed behavioral signals (views, saves, applies) | < 1ms |

### Cold Start Handling
New users with no interaction history get a **neutral 0.5 personalization score**, so matching is driven entirely by skill overlap and semantic relevance until behavioral signals accumulate.

---

## 🖥 Frontend Pages

| Page | Route | Description |
|------|-------|-------------|
| **Landing** | `/` | Hero + upload zone + auth modal (login/register) |
| **Parsing** | `/parsing` | Real-time SSE progress (5 animated steps) |
| **Profile Confirm** | `/profile/confirm` | Review AI-extracted data before saving |
| **Jobs Feed** | `/jobs` | Ranked job cards with match scores |
| **Job Detail** | `/jobs/[id]` | Full job description + AI match analysis |
| **Profile** | `/profile` | LinkedIn-style profile with skills/experience |
| **Dashboard** | `/dashboard` | Metrics, activity feed, match trend chart |

---

## 🔐 Environment Variables

### Backend (`backend/.env`)
```env
# Database
DATABASE_URL=postgresql+asyncpg://rmuser:rmpass@localhost:5432/resumematch

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

# S3 / MinIO
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET_NAME=resumes

# AI
GEMINI_API_KEY=your-gemini-api-key

# App
APP_DEBUG=true
CORS_ORIGINS=http://localhost:3000
```

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

## 🧪 Testing

```bash
cd backend

# Run all tests
pytest -v

# Run specific test
pytest tests/test_auth.py -v

# With coverage
pytest --cov=app --cov-report=html
```

---

## 🐳 Deployment

### Docker Compose (Full Stack)
```bash
docker-compose up -d
```

This starts:
- **PostgreSQL 16** (port 5432) with pgvector extension
- **Redis** (port 6379)
- **MinIO** (port 9000, console: 9001)

### Production Checklist
- [ ] Change `JWT_SECRET_KEY` to a cryptographically random value
- [ ] Set `APP_DEBUG=false`
- [ ] Configure proper `CORS_ORIGINS`
- [ ] Set up SSL/TLS termination
- [ ] Configure PostgreSQL connection pooling
- [ ] Set up log aggregation
- [ ] Add rate limiting middleware

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using FastAPI, Next.js, and Google Gemini AI**

</div>
