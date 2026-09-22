# TalentSphere Database ER Diagram & Schema Specification

## Database Architecture Overview
TalentSphere uses PostgreSQL as its primary database (with automatic SQLite dev fallback).

## Entity Relationship (ER) Summary

```text
+----------------+          +-------------------+          +--------------------+
|  User (custom) | -------> | Employee Profile  | -------> | Department / Desig |
+----------------+          +-------------------+          +--------------------+
        |                             |                             |
        v                             v                             v
+----------------+          +-------------------+          +--------------------+
| AuditLog       |          | AttendanceRecord  |          | Project / Tasks    |
+----------------+          +-------------------+          +--------------------+
                                      |                             |
                                      v                             v
                            +-------------------+          +--------------------+
                            | Payslip / Salary  |          | AI Skill Gap Analysis|
                            +-------------------+          +--------------------+
```

## Core Indexing Strategy

To maintain sub-50ms response times at scale, indexes are applied on frequently queried foreign keys and search columns:

1. `accounts_user.role`: Indexed for fast RBAC role checks.
2. `employees_employee.employee_id`, `email`: Unique indexes.
3. `employees_employee.manager_id`, `department_id`: Indexed for hierarchy queries.
4. `attendance_attendancerecord.employee_id`, `date`: Composite index `(employee, date)` for quick daily lookups.
5. `tasks_task.project_id`, `status`: Composite index for Kanban board queries.
6. `audit_logs_auditlog.action`, `timestamp`: Index for compliance searching.
