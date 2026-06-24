# Library Management System v2.0

A modern, role-based library management system built with FastAPI, PostgreSQL, and featuring advanced user authentication with OTP verification and admin approval workflow.

## 🎯 Features

### Authentication & Authorization
- ✅ User registration with email OTP verification
- ✅ Role-based access control (Admin & User)
- ✅ Admin approval workflow before user can login
- ✅ JWT token-based authentication
- ✅ Refresh token mechanism
- ✅ Secure password hashing

### User Management
- ✅ User profile management (view, update, delete)
- ✅ Admin can search users by name, email, username
- ✅ Admin approval/rejection of new users
- ✅ User account deactivation

### Book Management
- ✅ Complete CRUD operations for books (Admin)
- ✅ Book search by title, author, ISBN, category
- ✅ Book listing with pagination
- ✅ Filter by category
- ✅ Soft delete books
- ✅ Track available copies

### Technical Features
- ✅ PostgreSQL database
- ✅ pgAdmin for database management
- ✅ Async/await operations
- ✅ Comprehensive error handling
- ✅ API documentation (Swagger UI)
- ✅ CORS support

## 🏗️ Project Structure

```
library_system/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/
│   │       │   ├── auth.py          # Authentication endpoints
│   │       │   ├── books.py         # Book management endpoints
│   │       │   └── users.py         # User management endpoints
│   │       ├── dependencies.py       # Auth dependencies
│   │       └── router.py            # API router
│   ├── core/
│   │   ├── config.py                # Configuration
│   │   ├── security.py              # JWT & Password handling
│   │   └── exceptions.py            # Custom exceptions
│   ├── db/
│   │   └── session.py               # Database session
│   ├── models/
│   │   ├── user.py                  # User model
│   │   └── book.py                  # Book model
│   ├── schemas/
│   │   ├── auth.py                  # Auth schemas
│   │   ├── user.py                  # User schemas
│   │   └── book.py                  # Book schemas
│   ├── services/
│   │   ├── auth_service.py          # Authentication logic
│   │   ├── user_service.py          # User management logic
│   │   ├── book_service.py          # Book management logic
│   │   ├── otp_service.py           # OTP generation & verification
│   │   └── email_service.py         # Email sending
│   └── main.py                      # Application entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- pgAdmin 4


### Local Development

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment:**
```bash
cp .env.example .env
# Edit .env and set DATABASE_URL to your PostgreSQL connection
```

4. **Run migrations:**

```bash
alembic upgrade head

5. **Run application:**
```bash
uvicorn app.main:app --reload
```

## 📋 API Endpoints

### Authentication Endpoints

#### Register
```
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "full_name": "John Doe",
  "phone": "+1234567890"
}

Response:
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_approved": false,
  "is_email_verified": false,
  ...
}
```

#### Verify Email OTP
```
POST /api/v1/auth/verify-email
Content-Type: application/json

{
  "email": "john@example.com",
  "otp_code": "123456"
}

Response:
{
  "message": "Email verified successfully",
  "email_verified": true,
  "user_id": 1
}
```

#### Login
```
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=securepass123

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_role": "user",
  "user_id": 1,
  "username": "john_doe"
}
```

#### Check Approval Status
```
GET /api/v1/auth/approval-status/{user_id}

Response:
{
  "user_id": 1,
  "is_approved": false,
  "email_verified": true,
  "can_login": false,
  "rejection_reason": null
}
```

### User Profile Endpoints

#### Get My Profile
```
GET /api/v1/users/profile/me
Authorization: Bearer {access_token}

Response: UserDetailResponse
```

#### Update My Profile
```
PATCH /api/v1/users/profile/me
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "full_name": "John Updated",
  "phone": "+9876543210",
  "bio": "A book lover"
}
```

#### Delete My Account
```
DELETE /api/v1/users/profile/me
Authorization: Bearer {access_token}
```

### Book Endpoints

#### List Books
```
GET /api/v1/books/?skip=0&limit=20
Authorization: Bearer {access_token}
```

#### Search Books
```
GET /api/v1/books/search?q=harry&skip=0&limit=20
Authorization: Bearer {access_token}

Searches by: title, author, ISBN, category
```

#### Get Book
```
GET /api/v1/books/{book_id}
Authorization: Bearer {access_token}
```

#### Create Book (Admin Only)
```
POST /api/v1/books/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "title": "Harry Potter",
  "author": "J.K. Rowling",
  "isbn": "9780439135959",
  "description": "...",
  "category": "Fantasy",
  "publisher": "Bloomsbury",
  "publication_year": 1997,
  "pages": 309,
  "total_copies": 5,
  "available_copies": 3
}
```

#### Update Book (Admin Only)
```
PATCH /api/v1/books/{book_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "available_copies": 2,
  ...
}
```

#### Delete Book (Admin Only)
```
DELETE /api/v1/books/{book_id}
Authorization: Bearer {admin_token}
```

### Admin Endpoints

#### List All Users
```
GET /api/v1/users/?skip=0&limit=20
Authorization: Bearer {admin_token}
```

#### Search Users
```
GET /api/v1/users/admin/search?q=john&skip=0&limit=20
Authorization: Bearer {admin_token}

Searches by: username, email, full_name
```

#### List Pending Approvals
```
GET /api/v1/users/admin/pending-approvals
Authorization: Bearer {admin_token}
```

#### Approve User
```
POST /api/v1/users/admin/approve/{user_id}
Authorization: Bearer {admin_token}
```

#### Reject User
```
POST /api/v1/users/admin/reject/{user_id}?rejection_reason=Verified+multiple+accounts
Authorization: Bearer {admin_token}
```

## 🔐 Authentication Flow

### User Registration & Login Flow

```
1. User Registers
   ↓
2. OTP sent to email
   ↓
3. User verifies email with OTP
   ↓
4. Account created but NOT approved
   ↓
5. Admin receives pending approval notification
   ↓
6. Admin reviews and approves/rejects user
   ↓
7. User receives approval/rejection email
   ↓
8. Only approved users can login
   ↓
9. Login returns access token with user role
```

## 🔑 Environment Variables

Create `.env` file from `.env.example`:

```env
# App Settings
APP_NAME=Library Management System
APP_ENV=development
DEBUG=True

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=hello
DB_USER=postgres
DB_PASSWORD=your_password

# Security
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OTP
OTP_EXPIRY_MINUTES=10
OTP_LENGTH=6

# Email (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=app-password

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 📊 Database Access

### PostgreSQL
- **Host:** localhost
- **Port:** 5432
- **Username:** library_user (or as per .env)
- **Password:** library_password (or as per .env)
- **Database:** library_db (or as per .env)

### pgAdmin
- **URL:** http://localhost:5050
- **Email:** admin@library.com
- **Password:** admin

#### Adding Database Connection in pgAdmin:
1. Right-click "Servers" → Register → Server
2. **General Tab:**
   - Name: `PostgreSQL`
3. **Connection Tab:**
   - Hostname: `loaclhost` (or your DB host)
   - Port: `5432`
   - Username: `library_user`
   - Password: `library_password`
   - Database: `library_db`
4. Click Save

## 🧪 Testing with Swagger UI

1. Go to http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in required parameters
4. Click "Execute"

### Test Workflow:
1. **Register** → POST /api/v1/auth/register
2. **Verify Email** → POST /api/v1/auth/verify-email
3. **Check Status** → GET /api/v1/auth/approval-status/{user_id}
4. *Admin approves user*
5. **Login** → POST /api/v1/auth/login
6. **Get Profile** → GET /api/v1/users/profile/me
7. **List Books** → GET /api/v1/books/
8. **Search Books** → GET /api/v1/books/search?q=test

## 🛠️ Development

### Database Migrations (Alembic)

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Downgrade
alembic downgrade -1
```

## 📝 Notes

### OTP Verification
- OTP is currently logged to console (for development)
- To enable actual email sending, configure SMTP credentials in .env
- Modify `email_service.py` to implement your email provider

### Admin Account
- First admin user should be created manually in database:
```sql
INSERT INTO users (username, email, hashed_password, role, is_approved, is_active, is_email_verified, full_name, created_at, updated_at)
VALUES ('admin', 'admin@example.com', '$2b$12$...', 'admin', true, true, true, 'Admin User', NOW(), NOW());
```

Or use the API with a script to create the first admin.

### Security Notes
- Change `SECRET_KEY` in production
- Use strong database passwords
- Enable HTTPS in production
- Implement rate limiting for auth endpoints
- Add request logging and monitoring

## 🐛 Troubleshooting

### Database Connection Error
```
- Ensure PostgreSQL service is running.
- Verify database credentials in `.env`.
- Check if the database exists.
```

### OTP Not Received
```
- Check terminal logs.
- Verify SMTP credentials.
- Ensure email settings are configured correctly.
```

### Port Already in Use
```
- stop conflicting services
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [JWT Documentation](https://jwt.io/)

## 📄 License

MIT License - feel free to use this project as a template.

## 🤝 Support

For issues or questions, please create an issue in the repository.

---

**Made with ❤️ by Priyanshii**
