# Setup Instructions - Library Management System v2.0

## 📋 What's New in v2.0

This is a complete refactor of your library system with the following changes:

### ✅ Removed
- ❌ Loan system (all loan-related models, routes, schemas, services)

### ✅ Added
- ✅ Role-based authorization (ADMIN and USER roles)
- ✅ Email OTP verification for user registration
- ✅ Admin approval workflow (users must be approved before login)
- ✅ Login response includes user role (admin or user)
- ✅ User profile management (view, update, delete)
- ✅ Search users and books by name/email/username
- ✅ PostgreSQL database setup
- ✅ pgAdmin included in Docker Compose
- ✅ Comprehensive API documentation

## 🚀 Quick Start (Recommended - Docker)

### Step 1: Setup Environment
```bash
cd library_system_updated
cp .env.example .env
```

### Step 2: Start Services
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- pgAdmin (port 5050)
- FastAPI application (port 8000)

### Step 3: Access the System

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Database Management:**
- pgAdmin: http://localhost:5050
  - Email: admin@library.com
  - Password: admin

**Health Check:**
- http://localhost:8000/health

---

## 🔧 Manual Setup (Without Docker)

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- pip

### Step 1: Install PostgreSQL

**On macOS (Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**On Windows:**
Download from https://www.postgresql.org/download/windows/

### Step 2: Create Database and User

```bash
# Login to PostgreSQL
psql -U postgres

# Create user and database
CREATE USER library_user WITH PASSWORD 'library_password';
CREATE DATABASE library_db OWNER library_user;

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;

# Exit
\q
```

### Step 3: Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` file:
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=library_user
DB_PASSWORD=library_password
DB_NAME=library_db
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### Step 6: Run Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

---

## 📱 User Authentication Flow

### 1. User Registration

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe",
    "phone": "+1234567890"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_approved": false,
  "is_email_verified": false,
  "role": "user"
}
```

**What happens:**
- User account is created
- OTP is sent to email
- User account is marked as not approved

### 2. Verify Email with OTP

**Check logs/console for OTP code** (in development):
```bash
# Look for: "OTP Email would be sent to john@example.com"
# Look for: "OTP Code: 123456"
```

```bash
curl -X POST http://localhost:8000/api/v1/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "otp_code": "123456"
  }'
```

### 3. Admin Approval (Required!)

**Admin needs to approve the user:**

First, login as admin:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin_password"
```

Then approve the pending user:
```bash
curl -X POST http://localhost:8000/api/v1/users/admin/approve/1 \
  -H "Authorization: Bearer {admin_access_token}"
```

### 4. User Login

Now the user can login:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=SecurePass123!"
```

**Response includes user role:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_role": "user",
  "user_id": 1,
  "username": "john_doe"
}
```

---

## 👥 User Roles

### USER Role
- ✅ View own profile
- ✅ Update own profile
- ✅ Delete own account
- ✅ View books
- ✅ Search books
- ❌ Cannot manage other users
- ❌ Cannot manage books (CRUD)
- ❌ Cannot approve users

### ADMIN Role
- ✅ All USER permissions
- ✅ View all users
- ✅ Search users
- ✅ Approve/Reject users
- ✅ Deactivate users
- ✅ Create books
- ✅ Update books
- ✅ Delete books
- ✅ Manage all users

---

## 📚 Main API Endpoints

### Authentication
```
POST   /api/v1/auth/register              Register new user
POST   /api/v1/auth/verify-email          Verify email with OTP
POST   /api/v1/auth/resend-otp            Resend OTP code
POST   /api/v1/auth/login                 Login
POST   /api/v1/auth/refresh               Refresh token
POST   /api/v1/auth/logout                Logout
GET    /api/v1/auth/me                    Get current user
GET    /api/v1/auth/approval-status/{id}  Check approval status
```

### User Profile
```
GET    /api/v1/users/profile/me           Get my profile
PATCH  /api/v1/users/profile/me           Update my profile
DELETE /api/v1/users/profile/me           Delete my account
```

### Books
```
GET    /api/v1/books/                     List books
GET    /api/v1/books/search?q=...         Search books
GET    /api/v1/books/{id}                 Get book
POST   /api/v1/books/                     Create book (Admin)
PATCH  /api/v1/books/{id}                 Update book (Admin)
DELETE /api/v1/books/{id}                 Delete book (Admin)
```

### Admin Only - Users
```
GET    /api/v1/users/                     List all users
GET    /api/v1/users/admin/search?q=...   Search users
GET    /api/v1/users/admin/pending-approvals  List pending approval
POST   /api/v1/users/admin/approve/{id}   Approve user
POST   /api/v1/users/admin/reject/{id}    Reject user
DELETE /api/v1/users/admin/{id}           Deactivate user
```

---

## 🔑 Creating First Admin User

### Option 1: Using Database

```sql
-- Connect to PostgreSQL
psql -U library_user -d library_db

-- Insert admin user
INSERT INTO users (username, email, hashed_password, role, is_approved, is_active, is_email_verified, full_name, created_at, updated_at)
VALUES ('admin', 'admin@library.com', '$2b$12$YjJ5RDVkTDgyYjZkZjc3ZWUzZjRjYWY0MGMwMzc4YjQ2YTBmMGY0YeYWhYhKm', 'admin', true, true, true, 'Admin User', NOW(), NOW());

-- Verify
SELECT * FROM users WHERE username = 'admin';
```

### Option 2: Using SQL Script

Create `create_admin.sql`:
```sql
-- Password: admin (bcrypt hash)
INSERT INTO users (username, email, hashed_password, role, is_approved, is_active, is_email_verified, full_name, created_at, updated_at)
VALUES ('admin', 'admin@library.com', '$2b$12$YjJ5RDVkTDgyYjZkZjc3ZWUzZjRjYWY0MGMwMzc4YjQ2YTBmMGY0YeYWhYhKm', 'admin', true, true, true, 'Admin User', NOW(), NOW());
```

Run:
```bash
psql -U library_user -d library_db -f create_admin.sql
```

Admin login credentials:
- Username: `admin`
- Password: `admin`

**⚠️ Change password after first login!**

---

## 🗄️ Database Schema

### Users Table
```sql
users
├── id (PRIMARY KEY)
├── username (UNIQUE)
├── email (UNIQUE)
├── full_name
├── phone
├── bio
├── hashed_password
├── otp_code (for email verification)
├── otp_created_at
├── is_email_verified
├── is_approved (requires admin approval)
├── approved_by (admin who approved)
├── approved_at
├── rejection_reason
├── role (ADMIN or USER)
├── is_active
├── refresh_token
├── created_at
└── updated_at
```

### Books Table
```sql
books
├── id (PRIMARY KEY)
├── title
├── author
├── isbn (UNIQUE)
├── description
├── category
├── publisher
├── publication_year
├── pages
├── total_copies
├── available_copies
├── is_active
├── created_at
└── updated_at
```

---

## 🧪 Testing Workflow

### Using Swagger UI (http://localhost:8000/docs)

1. **Register**
   - Endpoint: POST /api/v1/auth/register
   - Fill in all fields
   - Copy user ID from response

2. **Check Console for OTP**
   - Look for "OTP Code: XXXXXX"

3. **Verify Email**
   - Endpoint: POST /api/v1/auth/verify-email
   - Enter email and OTP

4. **Login as Admin** (for approval)
   - Endpoint: POST /api/v1/auth/login
   - Username: `admin`, Password: `admin`
   - Copy access_token

5. **Approve User**
   - Endpoint: POST /api/v1/users/admin/approve/{user_id}
   - Add Authorization: Bearer {admin_token}
   - Execute

6. **Login as User**
   - Endpoint: POST /api/v1/auth/login
   - Username: `john_doe`, Password: `SecurePass123!`
   - Copy access_token

7. **Get Profile**
   - Endpoint: GET /api/v1/users/profile/me
   - Add Authorization: Bearer {user_token}

8. **List Books**
   - Endpoint: GET /api/v1/books/
   - Add Authorization: Bearer {user_token}

---

## 🐛 Common Issues

### 1. "Database connection refused"
```
Solution: Ensure PostgreSQL is running
docker-compose ps  # Check if postgres is running
docker-compose logs postgres  # View logs
```

### 2. "Email not verified"
```
Solution: Must verify email first
1. Check console/logs for OTP code
2. Call POST /api/v1/auth/verify-email with OTP
```

### 3. "Account pending admin approval"
```
Solution: Admin must approve the account
1. Login as admin
2. Call POST /api/v1/users/admin/approve/{user_id}
```

### 4. "Invalid token"
```
Solution: Token may have expired
1. Get new token: POST /api/v1/auth/refresh
2. Or login again: POST /api/v1/auth/login
```

### 5. Port already in use
```
Solution: Change port in docker-compose.yml or stop service
# Check what's using port 5432
lsof -i :5432

# Kill process or change port in docker-compose.yml
```

---

## 📊 pgAdmin Access

1. Go to http://localhost:5050
2. Login:
   - Email: `admin@library.com`
   - Password: `admin`
3. Add Server:
   - Right-click "Servers" → Register → Server
   - Name: PostgreSQL
   - Connection:
     - Host: `postgres` (or localhost if local)
     - Port: 5432
     - Username: `library_user`
     - Password: `library_password`
     - Database: `library_db`

---

## 🔒 Security Checklist

- [ ] Change SECRET_KEY in .env
- [ ] Change default admin password
- [ ] Enable HTTPS in production
- [ ] Set DEBUG=False in production
- [ ] Configure real email service (Gmail, SendGrid, etc.)
- [ ] Use strong database passwords
- [ ] Enable database backups
- [ ] Implement rate limiting
- [ ] Add request logging
- [ ] Monitor error logs
- [ ] Regular security updates

---

## 📞 Support

For detailed information, see README.md for:
- Full API documentation
- Environment variables
- Troubleshooting guide
- Development setup

For issues or questions, check:
1. README.md
2. Console/Application logs
3. API documentation (http://localhost:8000/docs)

---

**Ready to start? Run `docker-compose up -d` and visit http://localhost:8000/docs!**
