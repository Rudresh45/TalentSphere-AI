# TalentSphere — Technical Interview Explanation & Q&A Guide

This guide equips you with deep, architectural answers to impress interviewers when explaining **TalentSphere**.

---

## 1. High-Level Architectural Summary
> **Interviewer Question**: *"Can you describe the architecture of TalentSphere and why you chose this design?"*

**Answer**:
"TalentSphere is an enterprise-grade HR and Activity Intelligence Platform built using a clean, layered Django REST Framework backend and a modern React SPA frontend. I designed it around a modular separation of concerns:
- **Presentation Layer**: Thin DRF views that handle HTTP contracts and pagination.
- **Validation Layer**: DRF Serializers for strict input sanitization.
- **Business Layer**: Isolated Service functions (`services.py`) handling transactional business logic.
- **Query/Selector Layer**: Dedicated selectors (`selectors.py`) utilizing `select_related()` and `prefetch_related()` to eliminate N+1 database queries.
- **Security Pipeline**: Multi-tiered security enforcing JWT Auth, Scoped Rate Throttling, fine-grained Role-Based Access Control (RBAC), and Object-Level Authorization (`has_object_permission`) to prevent IDOR vulnerabilities.
- **AI Intelligence Engine**: Integrated spaCy NLP tokenization and scikit-learn TF-IDF vector cosine similarity for automated skill gap analysis and personalized course recommendations."

---

## 2. Security & IDOR Protection
> **Interviewer Question**: *"How do you prevent IDOR (Insecure Direct Object Reference) vulnerabilities in DRF?"*

**Answer**:
"I do not rely on frontend checks or URL obscure parameters. In DRF, I implement custom `BasePermission` classes that override `has_object_permission(self, request, view, obj)`.
For example, in `IsOwnerOrManagerOrHR`, the permission class checks:
1. Is the requesting user a Super Admin or HR Admin? If yes, allow.
2. Is the requesting user the owner of the object (`obj.user == request.user`)? If yes, allow.
3. Is the requesting user the direct manager of the employee (`obj.manager == user.employee_profile`)? If yes, allow.
Otherwise, DRF immediately denies access returning HTTP `403 Forbidden`."

---

## 3. JWT Authentication Lifecycle
> **Interviewer Question**: *"How did you configure SimpleJWT and handle token expiration?"*

**Answer**:
"I configured `djangorestframework-simplejwt` with short-lived Access Tokens (15 minutes) and longer-lived Refresh Tokens (7 days).
On the frontend, I built a centralized Axios interceptor. When an API call returns `401 Unauthorized`, the interceptor pauses execution, calls `/api/v1/auth/refresh/` using the refresh token, updates local storage with the new access token, and retries the failed request seamlessly."

---

## 4. AI & NLP Skill Gap Matching Algorithm
> **Interviewer Question**: *"How does your AI Skill Gap Engine work under the hood?"*

**Answer**:
"The AI engine takes employee skills and target role requirements, normalizes tokens via regex/spaCy string matching, and computes a TF-IDF (Term Frequency-Inverse Document Frequency) vector matrix using `scikit-learn`. It calculates cosine similarity between the employee vector and requirement vector to generate an exact match percentage. Missing skills are extracted and mapped to prioritized learning courses in our recommendation engine."

---

## 5. API Throttling & DDoS Defense
> **Interviewer Question**: *"How do you handle API rate limiting?"*

**Answer**:
"I implemented DRF `ScopedRateThrottle`. We enforce:
- Anonymous users: 20 requests/min
- Authenticated users: 100 requests/min
- Login endpoint: 5 requests/min (prevents brute-force)
- AI Intelligence endpoints: 10 requests/min (protects NLP resources)
When rate limits are exceeded, DRF returns HTTP `429 Too Many Requests` with a custom error format."
