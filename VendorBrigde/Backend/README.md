# VendorBridge Backend

Flask-based REST API backend for the VendorBridge procurement management system.

## Project Structure

```
Backend/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── routes/
│   └── auth.py        # Authentication routes
└── README.md          # This file
```

## Features

- **User Authentication**: Login and registration with JWT tokens
- **Password Security**: Bcrypt hashing for password storage
- **Role-Based Access**: Support for admin, vendor, and buyer roles
- **CORS Support**: Cross-origin requests from frontend
- **Token Verification**: Endpoint protection with JWT validation
- **Error Handling**: Comprehensive error responses

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Backend Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Test the API

The backend provides the following endpoints:

#### Authentication Endpoints

**Login**
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@vendorbridge.com",
  "password": "password123"
}

Response:
{
  "token": "eyJhbGc...",
  "user": {
    "id": "1",
    "name": "Test User",
    "email": "user@vendorbridge.com",
    "role": "admin"
  },
  "message": "Login successful"
}
```

**Register**
```
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "role": "vendor"
}

Response:
{
  "token": "eyJhbGc...",
  "user": {
    "id": "3",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "vendor"
  },
  "message": "Registration successful"
}
```

**Verify Token**
```
POST /api/auth/verify-token
Authorization: Bearer <token>

Response:
{
  "valid": true,
  "user": {...},
  "message": "Token is valid"
}
```

**Get Profile**
```
GET /api/auth/profile
Authorization: Bearer <token>

Response:
{
  "user": {
    "id": "1",
    "name": "Test User",
    "email": "user@vendorbridge.com",
    "role": "admin",
    "created_at": "2024-01-01T12:00:00"
  }
}
```

**Logout**
```
POST /api/auth/logout
Authorization: Bearer <token>

Response:
{
  "message": "Logout successful"
}
```

## Test Credentials

Use these credentials to test the login:

- **Admin User**
  - Email: `user@vendorbridge.com`
  - Password: `password123`

- **Vendor User**
  - Email: `vendor@example.com`
  - Password: `vendor123`

## Configuration

Edit `config.py` to customize:

- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT signing key
- `JWT_ACCESS_TOKEN_EXPIRES`: Token expiration time
- `CORS_ORIGINS`: Allowed CORS origins
- `DATABASE_URL`: Database connection string (for production)

## Environment Variables

Create a `.env` file in the Backend folder:

```
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///vendorbridge.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## Important Notes

- The current implementation uses an in-memory mock database
- For production, implement actual database (PostgreSQL, MySQL, etc.)
- Implement token blacklisting for logout functionality
- Set secure environment variables in production
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Add comprehensive logging

## Future Enhancements

- Database integration (SQLAlchemy)
- Email verification
- Password reset functionality
- Refresh token mechanism
- Two-factor authentication
- User profile management
- Vendor management
- RFQ (Request for Quotation) system
- Purchase order management
- Invoice tracking

## Troubleshooting

**Port 5000 already in use:**
```bash
lsof -ti:5000 | xargs kill -9
python app.py
```

**CORS errors:**
- Ensure frontend URL is in `CORS_ORIGINS` in config.py
- Check that Authorization header is included in requests

**Token errors:**
- Verify token format: `Authorization: Bearer <token>`
- Check token expiration
- Ensure JWT_SECRET_KEY matches between token generation and verification
