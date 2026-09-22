# TalentSphere Security Architecture & Compliance Guidelines

## 1. JWT Authentication Flow
```text
Client (Login Endpoint /api/v1/auth/login/)
        ↓
Validate Credentials & Active Status
        ↓
Generate Short-Lived Access Token (15 mins) & Refresh Token (7 days)
        ↓
Include Access Token in HTTP Header: "Authorization: Bearer <access_token>"
        ↓
On 401 Expiration: Client calls /api/v1/auth/refresh/ to receive new Access Token
```

## 2. Role-Based Access Control (RBAC) Matrix

| Role | User Mgmt | Dept Mgmt | Employee Mgmt | Recruitment | Attendance | Payroll | Task/Sprint | AI Analytics | Audit Logs |
|---|---|---|---|---|---|---|---|---|---|
| **SUPER_ADMIN** | Full | Full | Full | Full | Full | Full | Full | Full | Full |
| **HR_ADMIN** | Read | Full | Full | Full | Full | Full | Read | Read | Read |
| **HR_MANAGER** | - | Read | Team/Dept | Full | Dept | Dept | - | Read | - |
| **MANAGER** | - | Read | Team | - | Team | - | Full | Team | - |
| **ENGINEER** | - | - | Self | - | Self | Self | Assigned | Self | - |
| **EMPLOYEE** | - | - | Self | - | Self | Self | Self | Self | - |
| **RECRUITER** | - | - | - | Full | - | - | - | - | - |
| **FINANCE** | - | - | Read | - | - | Full | - | - | - |

## 3. Object-Level Authorization (IDOR Protection)
Frontend permission checks are purely for UI convenience. The backend enforces `has_object_permission` on every generic and viewset endpoint.

Example scenario:
`GET /api/v1/employees/42/`
If requester is `EMPLOYEE` with ID 10, the server denies access with `403 Forbidden`.

## 4. API Throttling & DDoS Protection
- **Anonymous Throttle**: 20 requests per minute
- **Authenticated Throttle**: 100 requests per minute
- **Login Endpoint Throttle**: 5 requests per minute
- **AI Intelligence Throttle**: 10 requests per minute

Exceeding rates yields HTTP `429 Too Many Requests`.

## 5. Security Headers & Production Checklist
- `SECURE_BROWSER_XSS_FILTER = True`
- `X_FRAME_OPTIONS = 'DENY'`
- `SECURE_CONTENT_TYPE_NOSNIFF = True`
- `CORS_ALLOW_ALL_ORIGINS = False` (explicit origin whitelist only)
- Sensitive credentials loaded strictly via environment variables (`.env`).
