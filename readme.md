# HRMS - Human Resource Management System

## Project Goal

Build a production-ready Human Resource Management System (HRMS) using only Django Framework.

The application should be suitable for small and medium organizations and follow enterprise-grade architecture, coding standards, security practices, and deployment requirements.

---

# Technology Stack

## Backend

* Python 3.12+
* Django 5.x
* PostgreSQL
* Django ORM
* Django Templates
* Django Forms
* Django Authentication
* Django Admin

## Deployment

* Render
* Gunicorn
* WhiteNoise

## Storage

* Local Storage (Development)
* Render Persistent Disk or AWS S3 (Production Ready)

---

# Strict Rules

## Allowed

* Django
* Django ORM
* Django Signals
* Django Middleware
* Django Templates
* PostgreSQL

## Not Allowed

* Django REST Framework
* FastAPI
* Flask
* React
* Angular
* Vue
* Next.js
* Celery
* Redis
* Microservices

Use Django's built-in capabilities whenever possible.

---

# Project Structure

```text
hrms/
│
├── config/
│   ├── settings/
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── core/
│   ├── accounts/
│   ├── employees/
│   ├── departments/
│   ├── attendance/
│   ├── leaves/
│   ├── payroll/
│   ├── recruitment/
│   ├── performance/
│   ├── assets/
│   ├── documents/
│   ├── holidays/
│   ├── shifts/
│   ├── notifications/
│   ├── reports/
│   └── auditlogs/
│
├── templates/
├── static/
├── media/
├── requirements/
├── manage.py
├── render.yaml
└── README.md
```

---

# Base Models

Create reusable abstract models.

## TimeStampedModel

```python
created_at
updated_at
```

## SoftDeleteModel

```python
is_deleted
deleted_at
```

All business models should inherit from TimeStampedModel.

---

# Authentication Module

App: accounts

## Custom User Model

Fields:

```python
email
employee_code
role
is_active
is_staff
is_superuser
last_login
created_at
updated_at
```

Authentication should use:

```python
AUTH_USER_MODEL
```

Email should be unique.

Username field should be email.

---

# Role Based Access Control

## Roles

### Super Admin

* Full access

### HR Manager

* Employee management
* Recruitment
* Payroll
* Reports

### Department Manager

* Team management
* Leave approvals
* Performance reviews

### Employee

* Self-service portal

Use Django Groups and Permissions.

---

# Employee Module

App: employees

## Employee

Fields:

```python
employee_id
user
first_name
last_name
gender
date_of_birth
phone
personal_email
joining_date
employment_type
employment_status
designation
department
manager
address
city
state
country
postal_code
profile_picture
```

Employment Types:

```text
Full Time
Part Time
Contract
Intern
```

Employment Status:

```text
Active
Probation
Notice Period
Resigned
Terminated
```

---

# Department Module

App: departments

## Department

Fields:

```python
name
code
description
head
```

Constraints:

```python
name unique
code unique
```

---

# Attendance Module

App: attendance

## Attendance

Fields:

```python
employee
date
check_in
check_out
working_hours
overtime_hours
status
remarks
```

Status:

```text
Present
Absent
Half Day
Leave
Holiday
```

Features:

* Daily Attendance
* Monthly Attendance
* Late Arrival Tracking
* Overtime Calculation

---

# Leave Management

App: leaves

## LeaveType

```python
name
days_per_year
is_paid
```

## LeaveRequest

```python
employee
leave_type
start_date
end_date
reason
status
approved_by
approved_at
```

Status:

```text
Pending
Approved
Rejected
Cancelled
```

Features:

* Leave Application
* Approval Workflow
* Leave Balance
* Leave History

---

# Payroll Module

App: payroll

## SalaryStructure

```python
employee
basic_salary
hra
allowances
deductions
effective_date
```

## Payroll

```python
employee
month
year
gross_salary
total_deductions
net_salary
generated_at
```

Features:

* Payroll Generation
* Payslip Generation
* Salary History

---

# Recruitment Module

App: recruitment

## JobOpening

```python
title
department
description
vacancies
status
```

## Candidate

```python
first_name
last_name
email
phone
resume
experience
status
```

Status:

```text
Applied
Screening
Interview
Selected
Rejected
Hired
```

---

# Performance Module

App: performance

## Review

```python
employee
reviewer
review_period
rating
comments
goals
review_date
```

Rating:

```text
1 Poor
2 Fair
3 Good
4 Very Good
5 Excellent
```

---

# Asset Management

App: assets

## Asset

```python
asset_code
name
category
purchase_date
purchase_price
status
```

## AssetAllocation

```python
asset
employee
allocated_date
returned_date
```

---

# Document Management

App: documents

## EmployeeDocument

```python
employee
document_type
file
expiry_date
```

Types:

```text
Resume
Offer Letter
Contract
Certificate
Government ID
Other
```

---

# Shift Management

App: shifts

## Shift

```python
name
start_time
end_time
grace_minutes
```

## EmployeeShift

```python
employee
shift
effective_from
```

---

# Holiday Module

App: holidays

## Holiday

```python
name
date
description
is_optional
```

---

# Notification Module

App: notifications

## Notification

```python
recipient
title
message
is_read
```

Generate notifications for:

* Leave Approval
* Leave Rejection
* Payroll Generated
* Performance Review Assigned
* Attendance Issues

---

# Reports Module

App: reports

Generate reports for:

* Employees
* Attendance
* Leaves
* Payroll
* Recruitment

Export formats:

* CSV
* Excel
* PDF

---

# Audit Logging

App: auditlogs

Track:

```python
user
action
model_name
object_id
ip_address
timestamp
```

Actions:

```text
Create
Update
Delete
Login
Logout
```

Use middleware and signals.

---

# Services Layer

Business logic must NOT exist inside views.

Structure:

```text
services/

employee_service.py

attendance_service.py

leave_service.py

payroll_service.py

notification_service.py
```

Views should call services.

---

# Signals

Implement Django signals for:

* Employee Created
* Leave Approved
* Leave Rejected
* Payroll Generated
* Notification Creation
* Audit Logging

---

# Dashboard

## Admin Dashboard

Widgets:

* Total Employees
* Active Employees
* Today's Attendance
* Pending Leaves
* Payroll Summary
* Open Positions

## Employee Dashboard

Widgets:

* My Attendance
* Leave Balance
* Upcoming Holidays
* Notifications
* Payslips

---

# Admin Configuration

For every model:

```python
list_display
list_filter
search_fields
ordering
readonly_fields
```

Use optimized queryset loading.

---

# Database Standards

Use PostgreSQL.

Requirements:

* Proper Foreign Keys
* Unique Constraints
* Indexes
* Transactions
* Query Optimization
* Select Related
* Prefetch Related

---

# Security

Enable:

* CSRF Protection
* Session Security
* XSS Protection
* Secure Password Validation
* Login Protection

Never disable Django security middleware.

---

# Testing

Use:

```python
django.test.TestCase
```

Coverage target:

```text
80%+
```

Test:

* Models
* Views
* Forms
* Services
* Permissions

---

# Health Check Endpoint

Create:

```text
/health/
```

Response:

```json
{
  "status": "ok"
}
```

Used by Render Health Check.

---

# Render Deployment

## Required Packages

```txt
Django
gunicorn
whitenoise
dj-database-url
psycopg[binary]
python-dotenv
Pillow
openpyxl
reportlab
```

---

## Static Files

```python
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

Use WhiteNoise.

---

## Database

Use:

```python
dj_database_url
```

Production database must use:

```python
DATABASE_URL
```

Environment variable.

---

## Environment Variables

```env
DEBUG=False

SECRET_KEY=

DATABASE_URL=

ALLOWED_HOSTS=.onrender.com

CSRF_TRUSTED_ORIGINS=https://*.onrender.com
```

---

## Build Command

```bash
pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate
```

---

## Start Command

```bash
gunicorn config.wsgi:application
```

---

## render.yaml

```yaml
services:
  - type: web
    name: hrms
    runtime: python

    buildCommand: |
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
      python manage.py migrate

    startCommand: |
      gunicorn config.wsgi:application

    envVars:
      - key: DEBUG
        value: False
```

---

# Development Roadmap

Phase 1

* Project Setup
* Authentication
* RBAC
* Departments

Phase 2

* Employees
* Attendance

Phase 3

* Leave Management

Phase 4

* Payroll

Phase 5

* Recruitment

Phase 6

* Performance

Phase 7

* Assets
* Documents

Phase 8

* Reports
* Audit Logs

Phase 9

* Deployment
* Production Hardening

---

# Final Deliverables

Generate:

1. Complete Django Project
2. PostgreSQL Integration
3. Custom User Model
4. All Modules
5. Templates
6. Forms
7. Services Layer
8. Signals
9. Tests
10. Admin Configuration
11. Render Deployment Files
12. Documentation
13. Seed Data
14. Production Configuration

The final system must be production-ready, maintainable, secure, scalable, and deployable directly to Render.
