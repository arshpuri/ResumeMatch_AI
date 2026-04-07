# ResumeMatch AI — Backend

## Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (for PostgreSQL, Redis, MinIO)

### Quick Start

1. **Start infrastructure:**
   ```bash
   cd ..
   docker-compose up -d postgres redis minio
   ```

2. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings (especially GEMINI_API_KEY)
   ```

4. **Run the backend:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. **Seed job data:**
   ```bash
   python -m scripts.seed_jobs
   ```

6. **Run tests:**
   ```bash
   pytest -v
   ```

### API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Architecture

```
app/
├── main.py           # FastAPI entrypoint
├── config.py         # Environment config
├── database.py       # SQLAlchemy async engine
├── dependencies.py   # Shared dependencies (auth, db)
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic request/response schemas
├── routers/          # FastAPI route handlers
├── services/         # Business logic layer
├── parsing/          # Resume parsing pipeline
├── matching/         # 3-layer recommendation engine
└── utils/            # JWT, S3, Redis helpers
```
