# HRMS (Human Resource Management System)

## Project Overview

Build a complete enterprise-grade Human Resource Management System (HRMS) using **only Django Framework**.

### Core Technology Stack

* Python 3.12+
* Django 5.x
* Django ORM
* Django Templates
* Django Authentication System
* Django Middleware
* Django Signals
* Django Forms
* Django Admin
* PostgreSQL

### Do NOT Use

* Django REST Framework
* FastAPI
* Flask
* React
* Vue
* Angular
* Next.js
* Celery (initial version)
* Microservices
* External Authentication Providers

Everything must be implemented using standard Django architecture.

---

# System Goals

Create a scalable HRMS capable of handling:

* Employee Management
* Organization Structure
* Attendance Management
* Leave Management
* Payroll
* Recruitment
* Performance Reviews
* Asset Management
* Document Management
* Shift Management
* Holidays
* Notifications
* Reports
* Audit Logs

---

# Architecture

Use Modular Monolithic Architecture.

```text
hrms/
│
├── config/
│
├── apps/
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
└── requirements/
```

---

# User Roles

Implement Role Based Access Control (RBAC).

## Roles

### Super Admin

Full system access.

### HR Manager

* Manage employees
* Manage recruitment
* Manage payroll
* Approve leave

### Department Manager

* View team members
* Approve leave
* Review performance

### Employee

* View profile
* Apply leave
* Check attendance
* View payslips

---

# Authentication Module

App: accounts

## Features

### User Model

Create Custom User Model.

Fields:

```python
email
employee_code
is_active
is_staff
role
created_at
updated_at
```

Use:

```python
AUTH_USER_MODEL
```

### Authentication

* Login
* Logout
* Password Reset
* Change Password
* Session Management

---

# Employee Module

App: employees

## Employee Model

Fields:

```python
employee_id
first_name
last_name
email
phone
date_of_birth
gender
joining_date
employment_type
employment_status
designation
department
manager
address
profile_picture
```

### Employment Types

* Full Time
* Part Time
* Contract
* Intern

### Employment Status

* Active
* Probation
* Notice Period
* Resigned
* Terminated

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
created_at
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
status
remarks
```

### Attendance Status

* Present
* Absent
* Half Day
* Holiday
* Leave

### Features

* Daily attendance
* Monthly attendance
* Late arrival tracking
* Overtime calculation

---

# Leave Management

App: leaves

## Leave Types

```python
Annual Leave
Sick Leave
Casual Leave
Maternity Leave
Paternity Leave
Unpaid Leave
```

## Leave Request

Fields:

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

### Status

```python
Pending
Approved
Rejected
Cancelled
```

### Features

* Apply leave
* Approve leave
* Leave balance tracking
* Leave history

---

# Payroll Module

App: payroll

## Salary Structure

Fields:

```python
employee
basic_salary
hra
allowances
deductions
effective_date
```

## Payroll Record

Fields:

```python
employee
month
year
gross_salary
deduction_amount
net_salary
generated_at
```

### Features

* Monthly payroll generation
* Payslip generation
* Salary history

---

# Recruitment Module

App: recruitment

## Job Position

Fields:

```python
title
department
description
vacancies
status
```

## Candidate

Fields:

```python
first_name
last_name
email
phone
resume
experience
status
```

### Candidate Status

```python
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

## Performance Review

Fields:

```python
employee
reviewer
review_period
rating
comments
goals
review_date
```

### Rating Scale

```python
1 - Poor
2 - Fair
3 - Good
4 - Very Good
5 - Excellent
```

---

# Asset Management

App: assets

## Asset

Fields:

```python
asset_code
name
category
purchase_date
value
status
```

## Asset Allocation

Fields:

```python
asset
employee
allocated_date
returned_date
```

---

# Document Management

App: documents

## Employee Documents

Fields:

```python
employee
document_type
file
uploaded_at
expiry_date
```

### Types

```python
Resume
Offer Letter
Contract
ID Proof
Certificate
Other
```

---

# Shift Management

App: shifts

## Shift

Fields:

```python
name
start_time
end_time
grace_minutes
```

## Employee Shift

Fields:

```python
employee
shift
effective_from
```

---

# Holiday Module

App: holidays

## Holiday

Fields:

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

Fields:

```python
recipient
title
message
is_read
created_at
```

### Events

Generate notifications for:

* Leave approval
* Leave rejection
* Payroll generation
* Attendance issues
* Performance review

---

# Reports Module

App: reports

Generate:

* Employee Reports
* Attendance Reports
* Leave Reports
* Payroll Reports
* Recruitment Reports

Support:

* PDF Export
* Excel Export
* CSV Export

---

# Audit Log Module

App: auditlogs

Track:

* Create
* Update
* Delete
* Login
* Logout

Fields:

```python
user
action
model_name
object_id
timestamp
ip_address
```

---

# Dashboard

## Admin Dashboard

Widgets:

* Total Employees
* Active Employees
* Pending Leave Requests
* Payroll Summary
* Attendance Summary
* Recruitment Pipeline

## Employee Dashboard

Widgets:

* Attendance Today
* Leave Balance
* Upcoming Holidays
* Recent Notifications
* Payslips

---

# Django Admin Requirements

Every model must:

* Have list_display
* Have list_filter
* Have search_fields
* Have ordering
* Have readonly fields where applicable

Create custom admin dashboards.

---

# Database Requirements

Use PostgreSQL.

Requirements:

* Proper Foreign Keys
* Indexes
* Unique Constraints
* Database Transactions
* Query Optimization

---

# Security Requirements

Implement:

* CSRF Protection
* XSS Protection
* SQL Injection Prevention
* Session Security
* Password Validation

Never disable Django security features.

---

# Coding Standards

## Model Rules

Every model should inherit:

```python
TimeStampedModel
```

Fields:

```python
created_at
updated_at
```

## Service Layer

Business logic must NOT be written inside views.

Structure:

```text
services/
    employee_service.py
    payroll_service.py
    attendance_service.py
```

---

# Signals

Use Django Signals for:

* Employee creation
* Leave approval notifications
* Payroll generation notifications
* Audit logging

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

# Documentation

Generate:

* ER Diagram
* Database Schema Documentation
* API Documentation (internal)
* Deployment Guide

---

# Deployment

Support:

* Docker
* Docker Compose
* Nginx
* Gunicorn
* PostgreSQL

Environment variables:

```env
DEBUG=False

SECRET_KEY=

DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=

ALLOWED_HOSTS=
```

---

# Deliverables

AI should generate:

1. Complete Django Project Structure
2. Models
3. Forms
4. Services
5. Views
6. URLs
7. Templates
8. Admin Configurations
9. Tests
10. Docker Setup
11. Deployment Files
12. Seed Data Scripts
13. Documentation

The final system should be production-ready, modular, maintainable, secure, and scalable while using only Django Framework and PostgreSQL.
