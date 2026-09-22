# TalentSphere — Enterprise HR & Activity Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-green)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.15%2B-red)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-18-blue)](https://react.dev/)
[![JWT](https://img.shields.io/badge/Authentication-JWT-orange)](https://jwt.io/)

TalentSphere is a production-grade **Enterprise HR & Activity Intelligence Platform** designed with a clean, layered REST API backend and a responsive modern React frontend.

---

## Architecture Overview

```text
React.js Frontend (Vite + Tailwind CSS)
        ↓
API Gateway / Django REST API
        ↓
Authentication & Permission Layer (JWT + RBAC + Object Permissions)
        ↓
View / API Layer (DRF ViewSets & Generic Views)
        ↓
Serializer / Validation Layer (DRF Serializers)
        ↓
Service Layer (Business Logic Services)
        ↓
Repository / Query Layer (Selectors & Django ORM)
        ↓
PostgreSQL / SQLite Database
```

---

## Core Features

- **RBAC & Security**: 8 Enterprise roles (`SUPER_ADMIN`, `HR_ADMIN`, `HR_MANAGER`, `MANAGER`, `ENGINEER`, `EMPLOYEE`, `RECRUITER`, `FINANCE`).
- **Object-Level Permissions**: Strict IDOR protection preventing unauthorized resource access.
- **API Throttling & Security Headers**: Rate-limiting login attempts, anonymous hits, and AI calls.
- **AI Skill Gap & Recommendation Engine**: Powered by spaCy NLP and scikit-learn match scoring.
- **Full HR Lifecycle**: Recruitment, Onboarding, Attendance, Payroll, Offboarding.
- **Engineering Management**: Kanban Board, Sprint Planning, Tasks, KPI Dashboards.
- **Quotation Generator**: Customer quote builder with dynamic discount/tax calculations.
- **Immutable Audit Logging**: Compliance audit trail recording high-risk mutations.

---

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 20+
- Git

### Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## API Documentation
Swagger UI is available at `/api/docs/` when the backend server is running.
