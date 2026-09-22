"""
TalentSphere AI Intelligence & Recommendation Engine
Uses TF-IDF Vectorization and Cosine Similarity (scikit-learn) + spaCy NLP tokenization
to compute Skill Gap Analysis and Personalized Learning Recommendations.
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ai_intelligence.models import SkillGapAnalysis, LearningRecommendation, PriorityLevel
from employees.models import Employee

# Pre-curated enterprise learning pathway database mapping skills to courses
RECOMMENDED_COURSE_CATALOG = {
    "fastapi": {"title": "FastAPI REST API Masterclass", "desc": "Build async high-performance APIs with FastAPI & Pydantic.", "priority": PriorityLevel.HIGH, "url": "https://learning.talentsphere.io/courses/fastapi"},
    "docker": {"title": "Containerization & Docker Fundamentals", "desc": "Containerize microservices, write Dockerfiles, and compose stacks.", "priority": PriorityLevel.HIGH, "url": "https://learning.talentsphere.io/courses/docker"},
    "aws": {"title": "AWS Cloud Practitioner & Solutions Architect", "desc": "Master IAM, EC2, S3, ECS, RDS, and Serverless cloud deployment.", "priority": PriorityLevel.HIGH, "url": "https://learning.talentsphere.io/courses/aws"},
    "postgresql": {"title": "Advanced PostgreSQL & Query Optimization", "desc": "Master indexing, query explain plans, partitioning, and ACID transactions.", "priority": PriorityLevel.HIGH, "url": "https://learning.talentsphere.io/courses/postgresql"},
    "kubernetes": {"title": "Kubernetes Orchestration in Production", "desc": "Deploy, scale, and manage containerized apps using K8s clusters.", "priority": PriorityLevel.HIGH, "url": "https://learning.talentsphere.io/courses/k8s"},
    "react": {"title": "Modern React.js & Redux Toolkit Architecture", "desc": "Build scalable React SPA UIs with custom hooks & state management.", "priority": PriorityLevel.MEDIUM, "url": "https://learning.talentsphere.io/courses/react"},
    "graphql": {"title": "GraphQL API Architecture with Python & React", "desc": "Design schema, resolvers, mutations, and subscriptions.", "priority": PriorityLevel.MEDIUM, "url": "https://learning.talentsphere.io/courses/graphql"},
    "ci/cd": {"title": "Enterprise CI/CD Pipelines with GitHub Actions", "desc": "Automate testing, linting, building, and automated deployment.", "priority": PriorityLevel.MEDIUM, "url": "https://learning.talentsphere.io/courses/cicd"},
    "system design": {"title": "Distributed Systems & Scalable Architecture", "desc": "Master caching, load balancing, message queues, and database sharding.", "priority": PriorityLevel.HIGH, "url": "https://learning.talentsphere.io/courses/system-design"},
}


def normalize_skill(skill: str) -> str:
    """Clean and normalize skill string."""
    return re.sub(r'[^a-zA-Z0-9\+/ ]', '', skill.strip().lower())


def analyze_skill_gap(*, employee: Employee, target_role: str, required_skills: list[str]) -> SkillGapAnalysis:
    """
    Executes AI Skill Gap Analysis using scikit-learn TF-IDF & Cosine Similarity.
    """
    employee_skills_raw = employee.skills or []
    if isinstance(employee_skills_raw, str):
        employee_skills_raw = [s.strip() for s in employee_skills_raw.split(',')]

    emp_skills_norm = [normalize_skill(s) for s in employee_skills_raw if s.strip()]
    req_skills_norm = [normalize_skill(s) for s in required_skills if s.strip()]

    # Exact and fuzzy skill matching
    matched_skills = []
    missing_skills = []

    for req_skill, orig_req in zip(req_skills_norm, required_skills):
        if any(emp_s == req_skill or req_skill in emp_s or emp_s in req_skill for emp_s in emp_skills_norm):
            matched_skills.append(orig_req)
        else:
            missing_skills.append(orig_req)

    # Compute TF-IDF Cosine Similarity score
    if emp_skills_norm and req_skills_norm:
        emp_doc = " ".join(emp_skills_norm)
        req_doc = " ".join(req_skills_norm)
        vectorizer = TfidfVectorizer().fit_transform([emp_doc, req_doc])
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
        match_percentage = round(float(cosine_sim * 100), 1)
    elif matched_skills and required_skills:
        match_percentage = round((len(matched_skills) / len(required_skills)) * 100, 1)
    else:
        match_percentage = 0.0

    analysis = SkillGapAnalysis.objects.create(
        employee=employee,
        target_role=target_role,
        match_percentage=match_percentage,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )

    # Generate Personalized Learning Recommendations for missing skills
    for missing in missing_skills:
        norm_m = normalize_skill(missing)
        catalog_entry = RECOMMENDED_COURSE_CATALOG.get(
            norm_m,
            {
                "title": f"Mastering {missing}",
                "desc": f"Comprehensive learning pathway to build expertise in {missing}.",
                "priority": PriorityLevel.MEDIUM,
                "url": f"https://learning.talentsphere.io/courses/{norm_m}"
            }
        )

        LearningRecommendation.objects.create(
            analysis=analysis,
            skill_gap=missing,
            course_title=catalog_entry["title"],
            description=catalog_entry["desc"],
            priority=catalog_entry["priority"],
            recommended_url=catalog_entry["url"]
        )

    return analysis
