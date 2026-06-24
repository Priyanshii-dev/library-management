# Project Structure Overview - Library Management System v2.0

## 📁 Complete File Structure

```
library_system_updated/
│
├── app/
│   ├── __init__.py                      # App package marker
│   ├── main.py                          # FastAPI application entry point
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── dependencies.py          # Auth dependencies (get_current_user, get_current_admin)
│   │       ├── router.py                # Main API router that includes all routes
│   │       └── routes/
│   │           ├── __init__.py
│   │           ├── auth.py              # Authentication routes (register, login, verify, logout, etc.)
│   │           ├── books.py             # Book routes (list, search, create, update, delete)
│   │           └── users.py             # User routes (profile, admin operations)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                    # App configuration (database, JWT, OTP, email settings)
│   │   ├── security.py                  # Password hashing, JWT token creation/validation
│   │   └── exceptions.py                # Custom exception classes
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py                   # Database session configuration, engine setup
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                      # User model (with OTP fields, approval workflow)
│   │   └── book.py                      # Book model (with book fields)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py                      # Auth schemas (register, login, OTP, token, etc.)
│   │   ├── user.py                      # User schemas (profile, update, list, etc.)
│   │   └── book.py                      # Book schemas (create, update, list, etc.)
│   │
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py              # Authentication logic (register, login, OTP verification)
│       ├── user_service.py              # User management (profile, search, approval)
│       ├── book_service.py              # Book management (CRUD, search)
│       ├── otp_service.py               # OTP generation and verification
│       └── email_service.py             # Email sending (OTP, approval notifications)
│
├── requirements.txt                     # Python dependencies
├── gunicorn.conf.py                     # Gunicorn configuration for production
├── .env.example                         # Environment variables template
├── README.md                            # Complete documentation
├── SETUP.md                             # Step-by-step setup instructions
└── PROJECT_STRUCTURE.md                 # This file
```

## 📋 Files Summary

### Core Application Files

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app initialization, middleware setup, exception handlers, lifespan events |
| `app/core/config.py` | Configuration management (DB, JWT, OTP, email, CORS) |
| `app/core/security.py` | Password hashing, JWT token creation/validation |
| `app/core/exceptions.py` | Custom HTTP exceptions for common errors |

### Database & Models

| File | Purpose |
|------|---------|
| `app/db/session.py` | AsyncEngine, async_sessionmaker, Base class, get_db dependency |
| `app/models/user.py` | User model with OTP fields, approval workflow, role enum |
| `app/models/book.py` | Book model for library books management |

### Schemas & Validation

| File | Purpose |
|------|---------|
| `app/schemas/auth.py` | TokenResponse, OTPRequest, LoginRequest, RegistrationRequest |
| `app/schemas/user.py` | UserOut, UserUpdate, UserListOut, UserDetailResponse, UserApprovalRequest |
| `app/schemas/book.py` | BookCreate, BookUpdate, BookOut, BookSearchResponse |

### Services & Business Logic

| File | Purpose |
|------|---------|
| `app/services/auth_service.py` | Register, login, OTP verification, token refresh, logout |
| `app/services/user_service.py` | Profile management, user search, admin approval/rejection |
| `app/services/book_service.py` | Book CRUD, search by title/author/ISBN/category |
| `app/services/otp_service.py` | OTP generation (6 digits), expiry validation |
| `app/services/email_service.py` | OTP email, approval/rejection email templates |

### API Routes

| File | Purpose |
|------|---------|
| `app/api/v1/router.py` | Main router that includes all sub-routers |
| `app/api/v1/dependencies.py` | get_current_user, get_current_admin auth dependencies |
| `app/api/v1/routes/auth.py` | Auth endpoints (register, verify, login, refresh, logout) |
| `app/api/v1/routes/books.py` | Book endpoints (list, search, create, update, delete) |
| `app/api/v1/routes/users.py` | User endpoints (profile, admin operations) |

### Configuration & Deployment

| File | Purpose |
|------|---------|
| `gunicorn.conf.py` | Production ASGI server configuration |
| `.env.example` | Environment variables template (copy to .env) |
| `requirements.txt` | Python package dependencies |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Complete features, setup, API docs, troubleshooting |
| `SETUP.md` | Step-by-step installation instructions |
| `PROJECT_STRUCTURE.md` | This file - project overview |

---

## 🔄 Key Changes from v1 to v2

### ✅ Added
- **User Model Enhancements:**
  - `otp_code`, `otp_created_at` - For email verification
  - `is_email_verified` - Email verification flag
  - `is_approved`, `approved_by`, `approved_at` - Admin approval workflow
  - `rejection_reason` - For rejected applications
  - `full_name`, `phone`, `bio` - User profile fields

- **New Services:**
  - `OTPService` - OTP generation and validation
  - `EmailService` - Email sending for OTP and approvals
  - `UserService` - User profile and admin operations (was only auth before)

- **Enhanced Routes:**
  - `/auth/register` - Now with OTP requirements
  - `/auth/verify-email` - New OTP verification endpoint
  - `/auth/approval-status` - Check if user is approved
  - `/users/profile/*` - User profile management
  - `/users/admin/*` - Admin user management operations

- **Configuration:**
  - `OTP_EXPIRY_MINUTES` - OTP timeout setting
  - `OTP_LENGTH` - OTP code length
  - Email SMTP settings
  - Admin approval flag

### 🔄 Modified
- **User Role Enum:** Changed from `ADMIN, MEMBER` → `ADMIN, USER`
- **Book Model:** added category and publisher fields
- **Auth Flow:** Now requires email verification + admin approval
- **Login Response:** Now includes `user_role` field (admin or user)
- **Database:** PostgreSQL instead of default (can still use SQLite locally)

---

## 📊 Database Schema

### Users Table Columns
```
id                  INTEGER PRIMARY KEY
username            VARCHAR(50) UNIQUE
email               VARCHAR(255) UNIQUE
full_name           VARCHAR(255)
phone               VARCHAR(20)
bio                 TEXT
hashed_password     VARCHAR(255)
otp_code            VARCHAR(6)
otp_created_at      DATETIME
is_email_verified   BOOLEAN (default: False)
is_approved         BOOLEAN (default: False)
approved_by         INTEGER (FK: admin user id)
approved_at         DATETIME
rejection_reason    TEXT
role                ENUM('admin', 'user')
is_active           BOOLEAN (default: True)
refresh_token       VARCHAR(512)
created_at          DATETIME
updated_at          DATETIME
```

### Books Table Columns
```
id                  INTEGER PRIMARY KEY
title               VARCHAR(255)
author              VARCHAR(255)
isbn                VARCHAR(20) UNIQUE
description         TEXT
category            VARCHAR(100)
publisher           VARCHAR(255)
publication_year    INTEGER
pages               INTEGER
total_copies        INTEGER
available_copies    INTEGER
is_active           BOOLEAN (default: True)
created_at          DATETIME
updated_at          DATETIME
```

---

## 🔐 Authentication Flow Diagram

```
User Registration
    ↓
Email OTP Sent (to console in dev)
    ↓
User Verifies Email with OTP
    ↓
User Account Created (not approved yet)
    ↓
Admin Reviews Pending Users
    ↓
[Admin Approves] or [Admin Rejects]
    ↓
[If Approved] User Receives Approval Email
    ↓
User Can Login
    ↓
Login Returns Access Token with Role (admin/user)
    ↓
User Can Access API Based on Role
```

---

## 🎯 Role-Based Access Control

### USER Role
- View own profile
- Update own profile  
- Delete own account
- View books
- Search books
- View others' profiles (if needed via API)

### ADMIN Role
- All USER permissions
- View all users
- Search users (by name, email, username)
- View pending approvals
- Approve users
- Reject/deactivate users
- Create books
- Update books
- Delete books
- Manage any user

---

## 📡 API Endpoint Categories

### Public Endpoints (No Auth Required)
```
POST /api/v1/auth/register
POST /api/v1/auth/verify-email
POST /api/v1/auth/resend-otp
POST /api/v1/auth/login
GET  /api/v1/auth/approval-status/{user_id}
```

### Protected Endpoints (Auth Required)
```
GET  /api/v1/auth/me
GET  /api/v1/books/
GET  /api/v1/books/search
GET  /api/v1/books/{id}
GET  /api/v1/users/profile/me
PATCH /api/v1/users/profile/me
DELETE /api/v1/users/profile/me
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
```

### Admin-Only Endpoints
```
POST /api/v1/books/
PATCH /api/v1/books/{id}
DELETE /api/v1/books/{id}
GET  /api/v1/users/
GET  /api/v1/users/admin/search
GET  /api/v1/users/admin/pending-approvals
POST /api/v1/users/admin/approve/{id}
POST /api/v1/users/admin/reject/{id}
DELETE /api/v1/users/admin/{id}
```

---

## 🚀 Deployment Ready

This project includes:
- ✅ PostgreSQL database
- ✅ pgAdmin for database management
- ✅ Environment-based configuration
- ✅ Production-ready ASGI server (Gunicorn)
- ✅ Health check endpoints
- ✅ Comprehensive error handling
- ✅ API documentation (Swagger UI)

---

## 📦 Dependencies

Key packages used:
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM with async support
- **asyncpg** - PostgreSQL async driver
- **Pydantic** - Data validation
- **python-jose** - JWT tokens
- **passlib** - Password hashing
- **pyotp** - OTP generation (alternative, can use random for 6-digit)

See `requirements.txt` for complete list.

---

## 🔧 Configuration Management

All configuration in `app/core/config.py`:
- Database connection (PostgreSQL)
- JWT settings (algorithm, expiry)
- OTP settings (length, expiry)
- Email settings (SMTP, from address)
- CORS origins
- App environment settings

Loaded from `.env` file (template: `.env.example`)

---

## 📝 Notes for Development

1. **OTP in Development:** Currently logged to console
   - Look for "OTP Code: XXXXXX" in logs
   - Configure email service in `email_service.py` for production

2. **First Admin User:** 
   - Created manually via SQL or
   - Create via API with special script (to implement)

3. **Email Service:**
   - Currently logging instead of sending
   - Implement SMTP in `email_service.py`
   - Supports Gmail, SendGrid, custom SMTP

4. **Database Migrations:**
   - Currently using SQLAlchemy's create_all
   - Alembic integration available for migrations

5. **Logging:**
   - Configured in `main.py`
   - Check console for OTP and debug info

---

**Version:** 2.0.0  
**Created:** 2024  
**Database:** PostgreSQL  
**Framework:** FastAPI + SQLAlchemy  
**Authentication:** JWT with OTP Verification
