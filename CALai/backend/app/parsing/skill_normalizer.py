"""
Skill normalization — from 02_resume_parsing_engine.md Step 4.
Maps 500+ skill aliases to canonical forms.
"""

SKILL_ALIASES: dict[str, list[str]] = {
    # Programming Languages
    "javascript": ["js", "javascript", "java script", "es6", "es2015", "es2020", "ecmascript"],
    "typescript": ["ts", "typescript", "type script"],
    "python": ["python", "python3", "py", "python 3"],
    "java": ["java", "java se", "java ee"],
    "csharp": ["c#", "csharp", "c sharp", ".net c#"],
    "cpp": ["c++", "cpp", "c plus plus"],
    "c": ["c language", "c programming"],
    "go": ["go", "golang", "go lang"],
    "rust": ["rust", "rust lang"],
    "ruby": ["ruby", "rb"],
    "php": ["php", "php7", "php8"],
    "swift": ["swift", "swift ui"],
    "kotlin": ["kotlin", "kt"],
    "scala": ["scala"],
    "r": ["r language", "r programming", "r stats"],
    "sql": ["sql", "structured query language"],
    "html": ["html", "html5", "html 5"],
    "css": ["css", "css3", "css 3", "cascading style sheets"],
    "bash": ["bash", "shell", "shell scripting", "sh"],
    "dart": ["dart"],

    # Frontend Frameworks
    "react": ["react", "reactjs", "react.js", "react js", "react 18", "react 19"],
    "nextjs": ["next.js", "nextjs", "next js", "next"],
    "angular": ["angular", "angularjs", "angular.js", "angular 2+"],
    "vue": ["vue", "vuejs", "vue.js", "vue js", "vue 3"],
    "svelte": ["svelte", "sveltekit"],
    "jquery": ["jquery", "j query"],
    "tailwindcss": ["tailwind", "tailwindcss", "tailwind css"],
    "bootstrap": ["bootstrap", "bootstrap 5"],
    "sass": ["sass", "scss"],

    # Backend Frameworks
    "nodejs": ["node", "node.js", "nodejs", "node js"],
    "express": ["express", "expressjs", "express.js"],
    "fastapi": ["fastapi", "fast api"],
    "django": ["django", "django rest", "drf"],
    "flask": ["flask"],
    "spring": ["spring", "spring boot", "springboot"],
    "rails": ["rails", "ruby on rails", "ror"],
    "laravel": ["laravel"],
    "aspnet": ["asp.net", "aspnet", ".net", "dotnet", ".net core"],

    # Databases
    "postgresql": ["postgresql", "postgres", "psql", "pg"],
    "mysql": ["mysql", "my sql"],
    "mongodb": ["mongodb", "mongo", "mongo db"],
    "redis": ["redis"],
    "elasticsearch": ["elasticsearch", "elastic", "elastic search", "es"],
    "sqlite": ["sqlite", "sqlite3"],
    "dynamodb": ["dynamodb", "dynamo db", "aws dynamodb"],
    "cassandra": ["cassandra", "apache cassandra"],
    "oracle": ["oracle", "oracle db"],
    "sqlserver": ["sql server", "mssql", "ms sql"],

    # Cloud & DevOps
    "amazon_web_services": ["aws", "amazon web services"],
    "google_cloud": ["gcp", "google cloud", "google cloud platform"],
    "azure": ["azure", "microsoft azure", "ms azure"],
    "docker": ["docker", "docker compose", "dockerfile"],
    "kubernetes": ["kubernetes", "k8s", "kube"],
    "terraform": ["terraform", "tf"],
    "ansible": ["ansible"],
    "jenkins": ["jenkins"],
    "github_actions": ["github actions", "gh actions"],
    "gitlab_ci": ["gitlab ci", "gitlab ci/cd"],
    "circleci": ["circleci", "circle ci"],
    "nginx": ["nginx"],
    "linux": ["linux", "ubuntu", "centos", "debian"],

    # Data & ML
    "machine_learning": ["ml", "machine learning", "machine-learning"],
    "deep_learning": ["deep learning", "dl"],
    "tensorflow": ["tensorflow", "tf", "tensor flow"],
    "pytorch": ["pytorch", "py torch", "torch"],
    "scikit_learn": ["scikit-learn", "sklearn", "scikit learn"],
    "pandas": ["pandas"],
    "numpy": ["numpy", "np"],
    "spark": ["spark", "apache spark", "pyspark"],
    "kafka": ["kafka", "apache kafka"],
    "airflow": ["airflow", "apache airflow"],
    "opencv": ["opencv", "cv2"],
    "nlp": ["nlp", "natural language processing"],
    "computer_vision": ["computer vision", "cv"],

    # Tools
    "git": ["git", "git/github", "github", "version control"],
    "figma": ["figma"],
    "jira": ["jira", "atlassian jira"],
    "postman": ["postman"],
    "vscode": ["vscode", "vs code", "visual studio code"],
    "graphql": ["graphql", "graph ql"],
    "rest_api": ["rest", "rest api", "restful", "restful api"],
    "grpc": ["grpc", "g rpc"],
    "websockets": ["websockets", "websocket", "ws"],
    "rabbitmq": ["rabbitmq", "rabbit mq"],
    "celery": ["celery"],

    # Soft Skills
    "leadership": ["leadership", "team leadership", "tech lead"],
    "communication": ["communication", "written communication", "verbal communication"],
    "problem_solving": ["problem solving", "problem-solving", "analytical"],
    "teamwork": ["teamwork", "team work", "collaboration", "team player"],
    "agile": ["agile", "scrum", "kanban", "agile methodology"],
    "project_management": ["project management", "pm", "project mgmt"],
}


def normalize_skills(raw_skills: list[str]) -> list[str]:
    """
    Map raw skill strings to canonical forms using the alias dictionary.
    Returns sorted, deduplicated list of canonical skill names.
    """
    normalized: set[str] = set()

    for skill in raw_skills:
        skill_lower = skill.lower().strip()
        if not skill_lower:
            continue

        matched = False
        for canonical, aliases in SKILL_ALIASES.items():
            if skill_lower in aliases:
                normalized.add(canonical)
                matched = True
                break

        if not matched:
            # Keep as-is with basic cleanup
            cleaned = skill_lower.replace("-", "_").replace(" ", "_")
            normalized.add(cleaned)

    return sorted(normalized)


def get_display_name(canonical: str) -> str:
    """Convert canonical skill name back to display-friendly format."""
    display_map = {
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "python": "Python",
        "react": "React",
        "nextjs": "Next.js",
        "nodejs": "Node.js",
        "tailwindcss": "Tailwind CSS",
        "postgresql": "PostgreSQL",
        "mongodb": "MongoDB",
        "amazon_web_services": "AWS",
        "google_cloud": "GCP",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "graphql": "GraphQL",
        "machine_learning": "Machine Learning",
        "csharp": "C#",
        "cpp": "C++",
        "vue": "Vue.js",
    }
    return display_map.get(canonical, canonical.replace("_", " ").title())
