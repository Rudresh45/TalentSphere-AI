# TalentSphere Architecture Specification

## Overview
TalentSphere is built using a clean layered REST API backend architecture with Django REST Framework (DRF) and a modern React SPA frontend.

## Clean Layered Architecture Diagram

```text
React.js Frontend (Vite, Tailwind CSS, Axios)
        ↓
API Gateway / Router (urls.py + DRF Spectacular OpenAPI)
        ↓
Security Middleware Layer (CORS, Throttling, Security Headers, Audit Logging)
        ↓
Authentication & Authorization Layer (JWT, RBAC Permissions, Object-Level Permissions)
        ↓
Views / Controllers (DRF Generic Views & ViewSets - Thin Views)
        ↓
Serializers & Validators (Input Validation, Data Transformation)
        ↓
Service Layer (services.py - Core Business Logic)
        ↓
Selector / Repository Layer (selectors.py - Database Queries & Optimization)
        ↓
PostgreSQL / Database Models (models.py - ORM)
```

## Security Layers Pipeline

Every incoming API request is processed through the following pipeline:

1. **HTTP/CORS Filter**: Validates allowed origins (`CORS_ALLOWED_ORIGINS`).
2. **Throttling Engine**: Enforces rate limits (Anon: 20/min, User: 100/min, Login: 5/min, AI: 10/min).
3. **JWT Authentication**: Validates Bearer access token signature & expiration.
4. **User Active & Role Check**: Ensures active user status and inspects role (`SUPER_ADMIN`, `HR_ADMIN`, `HR_MANAGER`, `MANAGER`, `ENGINEER`, `EMPLOYEE`, `RECRUITER`, `FINANCE`).
5. **DRF Permission Class**: Evaluates role-level access rules (e.g. `IsManager`, `IsFinance`).
6. **Object-Level Permission**: Checks `has_object_permission` to protect against IDOR vulnerabilities.
7. **Serializer Validation**: Strict field validation and format validation before business logic execution.
8. **Service Layer Execution**: Executes domain business logic.
9. **Audit Logging**: Asynchronously logs state mutations to immutable audit table.
