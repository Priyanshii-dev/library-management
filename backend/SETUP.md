# Library Management System - Setup Instructions

## 📋 System Requirements

This is a Library Management System with the following features:
- **Role-based access**: Admin and User roles
- **User Authentication**: Email OTP verification with admin approval workflow
- **Book Management**: Complete CRUD operations for admins
- **Borrowing System**: Users can borrow, return, and renew books
- **Dashboard**: Admin dashboard with key statistics
- **Search & Filter**: Search functionality for users and books

---

## 🔧 Prerequisites

Before you start, ensure you have:

- **Python 3.9+** installed
- **PostgreSQL 12+** installed and running
- **pip** (Python package manager)
- **Git** (optional, for cloning repository)
- A text editor (VS Code, PyCharm, etc.)

### Install PostgreSQL

**On macOS (Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**On Windows:**
1. Download from https://www.postgresql.org/download/windows/
2. Run the installer
3. Remember the password you set for `postgres` user
4. Add PostgreSQL bin folder to PATH

**Verify Installation:**
```bash
psql --version
```

---

## 📁 Project Structure

```
library_management_system/
├── app/
│   ├── models/           # Database models
│   ├── routes/           # API endpoints
│   ├── schemas/          # Request/Response schemas
│   ├── services/         # Business logic
│   ├── middleware/       # Authentication, authorization
│   ├── database/         # DB configuration
│   └── main.py           # Application entry point
├── migrations/           # Database migrations (Alembic)
├── tests/                # Unit and integration tests
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
└── SETUP.md             # This file
```

---

## 🚀 Installation Steps

### Step 1: Create PostgreSQL Database and User

```bash
# Access PostgreSQL
psql -U postgres

# Create a new user for the library system
CREATE USER library_user WITH PASSWORD 'library_password';

# Create the database
CREATE DATABASE library_db OWNER library_user;

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
GRANT USAGE ON SCHEMA public TO library_user;
GRANT CREATE ON SCHEMA public TO library_user;

# Exit PostgreSQL
\q
```

**Verify the connection:**
```bash
psql -U library_user -d library_db -h localhost
```

If you see `library_db=>` prompt, the connection is successful. Type `\q` to exit.

---

### Step 2: Clone/Setup Project Repository

```bash
# Navigate to your project directory
cd ~/projects

# Clone your repository (or create new project folder)
git clone <your-repo-url> library_management_system
cd library_management_system
```

Or manually create the project structure as shown above.

---

### Step 3: Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal.

---

### Step 4: Install Dependencies

Create `requirements.txt` with the following packages:

```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.1
python-multipart==0.0.6
email-validator==2.1.0
alembic==1.13.0
python-dotenv==1.0.0
```

Install them:
```bash
pip install -r requirements.txt
```

---

### Step 5: Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` file with your actual values:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=library_user
DB_PASSWORD=library_password
DB_NAME=library_db

# Application Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email Configuration (for OTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# Application
APP_NAME=Library Management System
DEBUG=True
ENVIRONMENT=development
```

**⚠️ Important Security Notes:**
- Change `SECRET_KEY` to a strong random string
- Use environment-specific values for production
- Never commit `.env` file to version control

---

### Step 6: Create Database Tables

Create database migration script or execute SQL directly:

**Option A: Using Python with SQLAlchemy**

In your `app/database.py`:
```python
from sqlalchemy import create_engine
from app.models import Base

DATABASE_URL = "postgresql://library_user:library_password@localhost:5432/library_db"
engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(bind=engine)
```

Run from Python shell:
```bash
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

**Option B: Using SQL directly**

Execute this SQL to create all tables:

```sql
-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'User',
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories Table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Books Table
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2),
    category_id INTEGER REFERENCES categories(id),
    publication_year INTEGER,
    total_quantity INTEGER NOT NULL DEFAULT 0,
    available_quantity INTEGER NOT NULL DEFAULT 0,
    availability VARCHAR(10) DEFAULT 'Yes',
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Book Borrow Table
CREATE TABLE book_borrow (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    book_id INTEGER NOT NULL REFERENCES books(id),
    borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE,
    renewed_at DATE,
    returned_at DATE,
    status VARCHAR(20) DEFAULT 'Borrowed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_books_category ON books(category_id);
CREATE INDEX idx_borrow_user ON book_borrow(user_id);
CREATE INDEX idx_borrow_book ON book_borrow(book_id);
CREATE INDEX idx_borrow_status ON book_borrow(status);
```

Execute:
```bash
psql -U library_user -d library_db -f schema.sql
```

---

### Step 7: Create Admin User

Connect to the database and insert the admin user:

```bash
psql -U library_user -d library_db
```

```sql
-- Insert admin user
-- Password: admin123 (use bcrypt hash in production)
INSERT INTO users (first_name, last_name, email, phone, password, role, status, created_at, updated_at)
VALUES (
    'Admin',
    'User',
    'admin@library.com',
    '+1234567890',
    '$2b$12$your-bcrypt-hash-here',  -- Use proper bcrypt hash
    'Admin',
    'Approved',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Verify
SELECT * FROM users WHERE email = 'admin@library.com';
```

**To generate bcrypt hash, use Python:**
```bash
python
>>> import bcrypt
>>> password = "admin123"
>>> hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
>>> print(hashed.decode())
# Copy this hash and use in INSERT statement
```

---

## ▶️ Running the Application

### Start the Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run the FastAPI application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete
```

### Access the Application

Open your browser and visit:

- **API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative Documentation (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 🔐 Authentication & User Flow

### 1. User Registration

**Endpoint:** `POST /api/v1/auth/register`

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "id": 2,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "status": "Pending",
  "message": "Registration successful. OTP sent to your email."
}
```

**What happens:**
- User account created with `Pending` status
- OTP sent to registered email
- User cannot login until approved

### 2. Email Verification (OTP)

**Endpoint:** `POST /api/v1/auth/verify-email`

```bash
# Check application logs for OTP code
curl -X POST http://localhost:8000/api/v1/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "otp_code": "123456"
  }'
```

### 3. Admin Approval (Required!)

**Login as Admin first:**

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@library.com",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_role": "Admin"
}
```

**Approve the pending user:**

```bash
curl -X POST http://localhost:8000/api/v1/users/2/approve \
  -H "Authorization: Bearer {admin_access_token}"
```

### 4. User Login

**Endpoint:** `POST /api/v1/auth/login`

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_role": "User"
}
```

---

## 📚 Main API Endpoints

### Authentication Endpoints
```
POST   /api/v1/auth/register              Register new user
POST   /api/v1/auth/verify-email          Verify email with OTP
POST   /api/v1/auth/resend-otp            Resend OTP code
POST   /api/v1/auth/login                 Login user
POST   /api/v1/auth/logout                Logout
GET    /api/v1/auth/me                    Get current user info
```

### User Management (Admin Only)
```
GET    /api/v1/users/                     List all users
GET    /api/v1/users/{id}                 Get user details
PATCH  /api/v1/users/{id}                 Update user info
DELETE /api/v1/users/{id}                 Delete user
GET    /api/v1/users/pending              Get pending approvals
POST   /api/v1/users/{id}/approve         Approve user
POST   /api/v1/users/{id}/reject          Reject user
```

### User Profile (Self)
```
GET    /api/v1/users/profile/me           Get my profile
PATCH  /api/v1/users/profile/me           Update my profile
DELETE /api/v1/users/profile/me           Delete my account
```

### Book Management
```
GET    /api/v1/books/                     List all books
GET    /api/v1/books/search?q=...         Search books
GET    /api/v1/books/{id}                 Get book details
POST   /api/v1/books/                     Create book (Admin only)
PATCH  /api/v1/books/{id}                 Update book (Admin only)
DELETE /api/v1/books/{id}                 Delete book (Admin only)
```

### Book Borrowing
```
POST   /api/v1/books/{id}/borrow          Borrow a book
POST   /api/v1/borrow/{id}/return         Return borrowed book
POST   /api/v1/borrow/{id}/renew          Renew borrowed book
GET    /api/v1/borrow/history             Get borrowing history
GET    /api/v1/borrow/active              Get active borrowings
```

### Admin Dashboard (Admin Only)
```
GET    /api/v1/admin/dashboard            Get dashboard statistics
GET    /api/v1/admin/books/overdue        Get overdue books
GET    /api/v1/admin/books/returned       Get returned books
GET    /api/v1/admin/books/borrowed       Get borrowed books
```

---

## 🧪 Testing Workflow

### Using Swagger UI (http://localhost:8000/docs)

**Step 1: Create a New User**
1. Click on `POST /api/v1/auth/register`
2. Click "Try it out"
3. Fill in the request body:
   ```json
   {
     "first_name": "Jane",
     "last_name": "Smith",
     "email": "jane@example.com",
     "phone": "+1987654321",
     "password": "SecurePass456!"
   }
   ```
4. Click "Execute"
5. Note the user ID from response

**Step 2: Verify Email**
1. Check application logs for OTP code
2. Click on `POST /api/v1/auth/verify-email`
3. Fill in email and OTP code from logs
4. Execute

**Step 3: Login as Admin**
1. Click on `POST /api/v1/auth/login`
2. Use credentials:
   - Email: `admin@library.com`
   - Password: `admin123`
3. Copy the access token from response
4. Click "Authorize" button at top and paste token

**Step 4: Approve the User**
1. Click on `POST /api/v1/users/{id}/approve` (replace {id} with user ID from Step 1)
2. Click "Execute"
3. User is now approved

**Step 5: User Login**
1. Clear the Authorization header
2. Login with new user credentials (from Step 1)
3. Copy the new access token

**Step 6: Test Book Operations**
1. Authorize with user token
2. Try: `GET /api/v1/books/` to list books
3. Try: `GET /api/v1/books/search?q=title` to search
4. Try: `POST /api/v1/books/{id}/borrow` to borrow a book

---

## 📊 Sample Data

### Add Categories

```sql
INSERT INTO categories (name, description) VALUES
('Fiction', 'Fiction books and novels'),
('Science Fiction', 'Science fiction and futuristic stories'),
('Non-Fiction', 'Educational and informational books'),
('Mystery', 'Mystery and thriller novels'),
('History', 'Historical books and biographies');
```

### Add Sample Books

```sql
INSERT INTO books (title, author, category_id, publication_year, total_quantity, available_quantity, price) VALUES
('The Hobbit', 'J.R.R. Tolkien', 1, 1937, 5, 5, 15.99),
('Dune', 'Frank Herbert', 2, 1965, 3, 3, 18.99),
('Sapiens', 'Yuval Noah Harari', 3, 2011, 4, 4, 25.99),
('The Da Vinci Code', 'Dan Brown', 4, 2003, 6, 6, 14.99),
('A Brief History of Time', 'Stephen Hawking', 3, 1988, 2, 2, 18.99);
```

---

## 🔧 Development Setup

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

**requirements-dev.txt:**
```txt
pytest==7.4.3
pytest-cov==4.1.0
black==23.12.0
flake8==6.1.0
mypy==1.7.1
```

### Run Tests

```bash
pytest tests/ -v --cov=app
```

### Code Formatting

```bash
black app/ tests/
```

### Linting

```bash
flake8 app/ tests/
```

---

## 🐛 Troubleshooting

### 1. "Database connection refused"

**Problem:** Cannot connect to PostgreSQL

**Solution:**
```bash
# Check if PostgreSQL is running
# macOS:
brew services list

# Ubuntu:
sudo systemctl status postgresql

# Windows:
# Check Services app for PostgreSQL

# If not running, start it:
# macOS:
brew services start postgresql

# Ubuntu:
sudo systemctl start postgresql
```

### 2. "No module named 'app'"

**Problem:** Python cannot find the app module

**Solution:**
```bash
# Make sure you're in the correct directory
pwd

# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### 3. "FATAL: password authentication failed"

**Problem:** Wrong database credentials

**Solution:**
```bash
# Check .env file for correct credentials
cat .env

# Test connection:
psql -U library_user -d library_db -h localhost

# If still fails, reset password:
psql -U postgres
ALTER USER library_user WITH PASSWORD 'new_password';
\q
```

### 4. "Email verification not working"

**Problem:** OTP not received

**Solution:**
```bash
# Check application logs for OTP code
# OTP is printed to console in development mode

# Update email configuration in .env with real email service
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 5. "Port 8000 already in use"

**Problem:** Another application is using port 8000

**Solution:**
```bash
# Find what's using the port
# macOS/Linux:
lsof -i :8000

# Kill the process:
kill -9 <PID>

# Or use a different port:
uvicorn app.main:app --reload --port 8001
```

### 6. "User status is 'Pending' but cannot login"

**Problem:** User hasn't been approved by admin

**Solution:**
```bash
# Admin must approve the user first
# Use: POST /api/v1/users/{user_id}/approve

# Or directly in database:
UPDATE users SET status = 'Approved' WHERE email = 'user@example.com';
```

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in `.env` to a strong random string
- [ ] Change default admin password
- [ ] Configure real email service (Gmail, SendGrid, etc.)
- [ ] Set `DEBUG=False` in production environment
- [ ] Use strong database password (change from `library_password`)
- [ ] Enable HTTPS/SSL
- [ ] Set up database backups
- [ ] Implement rate limiting on API endpoints
- [ ] Add request logging and monitoring
- [ ] Review SQL queries for injection vulnerabilities
- [ ] Set up environment-specific configurations
- [ ] Enable CORS only for trusted domains
- [ ] Implement API versioning

---

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 5432 |
| DB_USER | Database user | library_user |
| DB_PASSWORD | Database password | library_password |
| DB_NAME | Database name | library_db |
| SECRET_KEY | JWT secret key | your-secret-key |
| ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiry time | 30 |
| REFRESH_TOKEN_EXPIRE_DAYS | Refresh token expiry | 7 |
| SMTP_SERVER | Email server | smtp.gmail.com |
| SMTP_PORT | Email server port | 587 |
| SMTP_USER | Email account | your-email@gmail.com |
| SMTP_PASSWORD | Email password | your-app-password |
| FROM_EMAIL | Sender email | your-email@gmail.com |
| DEBUG | Debug mode | True/False |
| ENVIRONMENT | Environment type | development/production |

---

## 📞 Getting Help

1. **Check Application Logs:** Look for detailed error messages
2. **Review API Documentation:** Visit http://localhost:8000/docs
3. **Check Database:** Verify tables exist and have data
4. **Test with cURL:** Use curl commands from this guide
5. **Read README.md:** More detailed information

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] PostgreSQL is running
- [ ] Database `library_db` is created
- [ ] User `library_user` can connect to database
- [ ] All tables are created in database
- [ ] Admin user exists in database
- [ ] Virtual environment is activated
- [ ] All dependencies are installed
- [ ] `.env` file is configured correctly
- [ ] Application starts without errors
- [ ] Can access Swagger UI (http://localhost:8000/docs)
- [ ] Can login as admin
- [ ] Can register new user
- [ ] Can verify email with OTP
- [ ] Can approve users as admin
- [ ] Can login as regular user

---

## 🎉 You're Ready!

Your Library Management System is now fully set up and ready to use. Start developing and building amazing features!

**Quick Commands Reference:**

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
uvicorn app.main:app --reload

# Access Swagger UI
http://localhost:8000/docs

# Connect to database
psql -U library_user -d library_db

# Deactivate virtual environment
deactivate
```

---

**Last Updated:** 2026
**Version:** 1.0