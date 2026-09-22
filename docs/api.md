# TalentSphere API Documentation

All API endpoints are versioned under `/api/v1/`.
Interactive OpenAPI 3.0 / Swagger UI documentation is served live at `/api/docs/` when the backend server is running.

## 1. Authentication & User Management (`/api/v1/auth/`)

| Method | Endpoint | Description | Permission | Throttle |
|---|---|---|---|---|
| `POST` | `/api/v1/auth/login/` | Obtain Access & Refresh Tokens | AllowAny | 5/min |
| `POST` | `/api/v1/auth/refresh/` | Refresh Access Token | AllowAny | - |
| `POST` | `/api/v1/auth/logout/` | Blacklist Refresh Token | IsAuthenticated | - |
| `POST` | `/api/v1/auth/register/` | Register New User | AllowAny | - |
| `GET` | `/api/v1/auth/me/` | Current User Profile | IsAuthenticated | - |
| `PATCH` | `/api/v1/auth/me/` | Update Current User | IsAuthenticated | - |
| `POST` | `/api/v1/auth/change-password/` | Change Password | IsAuthenticated | - |
| `GET` | `/api/v1/auth/users/` | List All Users | IsHRAdmin | - |
| `PATCH` | `/api/v1/auth/users/{id}/role/` | Update User Role | IsSuperAdmin | - |

## 2. Departments & Designations (`/api/v1/departments/`)

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/v1/departments/` | List Departments | IsAuthenticated |
| `POST` | `/api/v1/departments/` | Create Department | IsHRAdmin |
| `GET` | `/api/v1/departments/designations/` | List Designations | IsAuthenticated |
| `POST` | `/api/v1/departments/designations/` | Create Designation | IsHRAdmin |

## 3. Employee Management (`/api/v1/employees/`)

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/v1/employees/` | List Employees | IsAuthenticated (Role Filtered) |
| `POST` | `/api/v1/employees/` | Onboard Employee | IsHRAdmin |
| `GET` | `/api/v1/employees/{id}/` | Retrieve Employee Detail | IsOwnerOrManagerOrHR (IDOR Protected) |
| `PATCH` | `/api/v1/employees/{id}/` | Update Employee | IsOwnerOrManagerOrHR |
| `GET` | `/api/v1/employees/me/` | Logged-in Employee | IsAuthenticated |
| `PATCH` | `/api/v1/employees/{id}/update_status/` | Update Status | IsHRAdmin |

## 4. Attendance Module (`/api/v1/attendance/`)

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `POST` | `/api/v1/attendance/clock-in/` | Clock In Today | IsAuthenticated |
| `POST` | `/api/v1/attendance/clock-out/` | Clock Out Today | IsAuthenticated |
| `POST` | `/api/v1/attendance/start-break/` | Start Break | IsAuthenticated |
| `POST` | `/api/v1/attendance/end-break/` | End Break | IsAuthenticated |
| `GET` | `/api/v1/attendance/my/` | My Attendance Logs | IsAuthenticated |
| `GET` | `/api/v1/attendance/team/` | Team Attendance Logs | IsManager |

## 5. Payroll Module (`/api/v1/payroll/`)

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/v1/payroll/structures/` | Salary Structures | IsFinance |
| `GET` | `/api/v1/payroll/payslips/` | All Payslips | IsFinance / IsHRAdmin |
| `GET` | `/api/v1/payroll/payslips/my/` | Employee Payslips | IsAuthenticated (Self Only) |

## 6. Engineering & Tasks (`/api/v1/projects/`, `/api/v1/tasks/`, `/api/v1/sprints/`)

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/v1/projects/` | Projects List | IsAuthenticated |
| `GET` | `/api/v1/tasks/` | Tasks List | IsAuthenticated |
| `GET` | `/api/v1/sprints/` | Sprints List | IsAuthenticated |

## 7. AI Intelligence (`/api/v1/ai/`)

| Method | Endpoint | Description | Permission | Throttle |
|---|---|---|---|---|
| `POST` | `/api/v1/ai/skill-gap/analyze/` | Run AI Skill Gap Analysis | IsAuthenticated | 10/min |
| `GET` | `/api/v1/ai/recommendations/` | Learning Recommendations | IsAuthenticated | 10/min |

## 8. Audit Logs (`/api/v1/audit-logs/`)

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/v1/audit-logs/` | List Security Audit Logs | IsHRAdmin / IsSuperAdmin |
