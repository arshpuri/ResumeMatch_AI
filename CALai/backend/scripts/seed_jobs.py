"""
Seed script — populates ~100 realistic job listings.
Run: python -m scripts.seed_jobs
"""

import asyncio
import uuid
import random
from datetime import datetime, timezone, timedelta

from sqlalchemy import select, func
from app.database import async_session_factory, engine, Base
import app.models  # noqa: F401
from app.models.job import Job


# ── Job templates ──────────────────────────────────────────

COMPANIES = [
    ("Google", "Mountain View, CA"),
    ("Meta", "Menlo Park, CA"),
    ("Apple", "Cupertino, CA"),
    ("Amazon", "Seattle, WA"),
    ("Microsoft", "Redmond, WA"),
    ("Netflix", "Los Gatos, CA"),
    ("Stripe", "San Francisco, CA"),
    ("Airbnb", "San Francisco, CA"),
    ("Spotify", "New York, NY"),
    ("Shopify", "Remote"),
    ("Vercel", "Remote"),
    ("Figma", "San Francisco, CA"),
    ("Datadog", "New York, NY"),
    ("Snowflake", "San Mateo, CA"),
    ("Coinbase", "Remote"),
    ("Discord", "San Francisco, CA"),
    ("Notion", "San Francisco, CA"),
    ("Slack", "San Francisco, CA"),
    ("Twilio", "San Francisco, CA"),
    ("Cloudflare", "Austin, TX"),
    ("HashiCorp", "Remote"),
    ("Atlassian", "Sydney, Australia"),
    ("HubSpot", "Cambridge, MA"),
    ("Square", "San Francisco, CA"),
    ("Palantir", "Denver, CO"),
    ("TechNova", "San Francisco, Hybrid"),
    ("DesignCo", "Remote"),
    ("StartupInc", "New York, On-site"),
    ("DataWorks", "Austin, TX"),
    ("CloudScale", "Remote"),
]

JOB_TEMPLATES = [
    {
        "title": "Senior Frontend Developer",
        "skills_required": ["React", "TypeScript", "Next.js", "CSS", "HTML"],
        "skills_preferred": ["GraphQL", "Testing", "CI/CD"],
        "experience_level": "senior",
        "job_type": "full-time",
        "salary_min": 150000,
        "salary_max": 220000,
        "description": "We are seeking an experienced Frontend Developer to build exceptional user interfaces. You will work with React, TypeScript, and Next.js to create responsive, performant web applications.",
        "responsibilities": [
            "Build and maintain complex UI components with React and TypeScript",
            "Collaborate with designers to implement pixel-perfect interfaces",
            "Optimize application performance and accessibility",
            "Write comprehensive tests and documentation",
            "Mentor junior developers and conduct code reviews",
        ],
    },
    {
        "title": "Full Stack Engineer",
        "skills_required": ["React", "Node.js", "PostgreSQL", "TypeScript"],
        "skills_preferred": ["Docker", "AWS", "Redis"],
        "experience_level": "mid",
        "job_type": "full-time",
        "salary_min": 120000,
        "salary_max": 180000,
        "description": "Join our team as a Full Stack Engineer working across the entire web stack. Build features from database to UI using modern technologies.",
        "responsibilities": [
            "Develop full-stack features using React and Node.js",
            "Design and implement RESTful APIs",
            "Manage PostgreSQL databases and write optimized queries",
            "Deploy and monitor applications in cloud environments",
        ],
    },
    {
        "title": "Backend Engineer (Python)",
        "skills_required": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "skills_preferred": ["Kubernetes", "Redis", "Kafka"],
        "experience_level": "mid",
        "job_type": "full-time",
        "salary_min": 130000,
        "salary_max": 190000,
        "description": "We need a Backend Engineer experienced in Python to build scalable microservices. You'll design APIs, work with databases, and ensure system reliability.",
        "responsibilities": [
            "Design and implement API endpoints using FastAPI",
            "Build scalable data processing pipelines",
            "Write unit and integration tests",
            "Monitor and optimize system performance",
        ],
    },
    {
        "title": "Machine Learning Engineer",
        "skills_required": ["Python", "TensorFlow", "PyTorch", "SQL"],
        "skills_preferred": ["Kubernetes", "Spark", "MLOps"],
        "experience_level": "senior",
        "job_type": "full-time",
        "salary_min": 170000,
        "salary_max": 250000,
        "description": "Build and deploy ML models at scale. Work on recommendation systems, NLP, and computer vision projects that impact millions of users.",
        "responsibilities": [
            "Develop and train machine learning models",
            "Build ML pipelines for training and inference",
            "Collaborate with data scientists on research projects",
            "Deploy models to production with monitoring",
        ],
    },
    {
        "title": "DevOps Engineer",
        "skills_required": ["Docker", "Kubernetes", "AWS", "Terraform"],
        "skills_preferred": ["Python", "Go", "Prometheus"],
        "experience_level": "mid",
        "job_type": "full-time",
        "salary_min": 140000,
        "salary_max": 200000,
        "description": "Manage and scale our cloud infrastructure. Implement CI/CD pipelines, monitoring, and ensure 99.99% uptime.",
        "responsibilities": [
            "Manage Kubernetes clusters and containerized deployments",
            "Implement infrastructure as code with Terraform",
            "Build and maintain CI/CD pipelines",
            "Monitor system health and respond to incidents",
        ],
    },
    {
        "title": "Frontend UI/UX Engineer",
        "skills_required": ["React", "Tailwind CSS", "Figma", "JavaScript"],
        "skills_preferred": ["Framer Motion", "Three.js", "Storybook"],
        "experience_level": "mid",
        "job_type": "full-time",
        "salary_min": 110000,
        "salary_max": 170000,
        "description": "Create beautiful, intuitive user interfaces. Work closely with our design team to bring wireframes to life with modern web technologies.",
        "responsibilities": [
            "Implement responsive UI designs from Figma mockups",
            "Build reusable component libraries",
            "Create smooth animations and transitions",
            "Conduct usability testing and iterate on designs",
        ],
    },
    {
        "title": "Data Engineer",
        "skills_required": ["Python", "SQL", "Spark", "Airflow"],
        "skills_preferred": ["Kafka", "Snowflake", "dbt"],
        "experience_level": "mid",
        "job_type": "full-time",
        "salary_min": 130000,
        "salary_max": 195000,
        "description": "Build and maintain data pipelines that process billions of events. Design data models and ensure data quality across the organization.",
        "responsibilities": [
            "Design and build data pipelines using Spark and Airflow",
            "Create and maintain data warehouse schemas",
            "Ensure data quality and implement monitoring",
            "Collaborate with analytics teams on data needs",
        ],
    },
    {
        "title": "Mobile Developer (React Native)",
        "skills_required": ["React Native", "TypeScript", "JavaScript"],
        "skills_preferred": ["iOS", "Android", "Firebase"],
        "experience_level": "mid",
        "job_type": "full-time",
        "salary_min": 120000,
        "salary_max": 175000,
        "description": "Build cross-platform mobile applications using React Native. Deliver polished apps for iOS and Android from a single codebase.",
        "responsibilities": [
            "Develop mobile features using React Native",
            "Ensure smooth performance across devices",
            "Integrate with backend APIs and third-party services",
            "Publish apps to App Store and Google Play",
        ],
    },
    {
        "title": "Security Engineer",
        "skills_required": ["Python", "Linux", "AWS", "Networking"],
        "skills_preferred": ["Penetration Testing", "SIEM", "Compliance"],
        "experience_level": "senior",
        "job_type": "full-time",
        "salary_min": 160000,
        "salary_max": 230000,
        "description": "Protect our systems and data. Conduct security assessments, implement controls, and build a security-first culture.",
        "responsibilities": [
            "Perform security assessments and penetration testing",
            "Implement security controls and monitoring",
            "Respond to security incidents",
            "Develop security policies and training",
        ],
    },
    {
        "title": "Platform Engineer",
        "skills_required": ["Go", "Kubernetes", "Docker", "Linux"],
        "skills_preferred": ["Rust", "gRPC", "Service Mesh"],
        "experience_level": "senior",
        "job_type": "full-time",
        "salary_min": 160000,
        "salary_max": 240000,
        "description": "Build the platform that powers our engineering teams. Design developer tools, improve deployment workflows, and scale infrastructure.",
        "responsibilities": [
            "Design and build internal developer platform",
            "Improve CI/CD pipelines and deployment workflows",
            "Build observability and monitoring tools",
            "Scale infrastructure to handle growing traffic",
        ],
    },
]


async def seed():
    """Seed the database with ~100 realistic job listings."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        # Check if jobs already exist
        count_result = await session.execute(select(func.count(Job.id)))
        existing = count_result.scalar() or 0
        if existing > 0:
            print(f"Database already has {existing} jobs. Skipping seed.")
            return

        jobs = []
        now = datetime.now(timezone.utc)

        for i in range(100):
            template = random.choice(JOB_TEMPLATES)
            company, base_location = random.choice(COMPANIES)

            # Randomize location
            is_remote = random.random() < 0.3
            if is_remote:
                location = "Remote"
            else:
                location = base_location

            # Randomize salary
            base_min = template["salary_min"]
            base_max = template["salary_max"]
            variation = random.uniform(0.8, 1.2)
            salary_min = int(base_min * variation)
            salary_max = int(base_max * variation)

            # Randomize posted date (within last 30 days)
            days_ago = random.randint(0, 30)
            posted = now - timedelta(days=days_ago)

            # Vary the title slightly
            title = template["title"]
            if random.random() < 0.3:
                prefix = random.choice(["Staff", "Lead", "Principal", "Senior"])
                if prefix not in title:
                    title = f"{prefix} {title.replace('Senior ', '')}"

            job = Job(
                title=title,
                company=company,
                location=location,
                is_remote=is_remote,
                description=template["description"],
                description_clean=template["description"],
                job_type=template["job_type"],
                experience_level=template["experience_level"],
                salary_min=salary_min,
                salary_max=salary_max,
                salary_currency="USD",
                skills_required=template["skills_required"],
                skills_preferred=template.get("skills_preferred", []),
                responsibilities=template.get("responsibilities", []),
                source="seed",
                posted_date=posted.date(),
                is_active=True,
            )
            jobs.append(job)

        session.add_all(jobs)
        await session.commit()
        print(f"✅ Seeded {len(jobs)} jobs successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
