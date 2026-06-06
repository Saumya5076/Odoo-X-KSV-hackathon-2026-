# VendorBridge - Odoo X KSV Hackathon 2026

Complete procurement management system with frontend and backend.

## Project Structure

```
VendorBrigde/
├── Frontend/
│   ├── index.html           # Landing page
│   ├── login.html           # Login page
│   ├── style.css            # Main styles
│   ├── css/
│   │   └── login.css        # Login page styles
│   └── js/
│       └── login.js         # Login page JavaScript
└── Backend/
    ├── app.py               # Flask application
    ├── config.py            # Configuration
    ├── requirements.txt     # Python dependencies
    ├── .env.example         # Environment variables template
    ├── routes/
    │   └── auth.py          # Authentication routes
    └── README.md            # Backend documentation
```

## Quick Start

### Frontend Setup

1. Navigate to the Frontend folder
2. Open `index.html` in a browser or use a local server:
   ```bash
   python3 -m http.server 8000 --directory VendorBrigde/Frontend
   ```
3. Visit `http://localhost:8000`

### Backend Setup

1. Install Python dependencies:
   ```bash
   cd VendorBrigde/Backend
   pip install -r requirements.txt
   ```

2. Run the Flask server:
   ```bash
   python app.py
   ```

3. The API will be available at `http://localhost:5000`

## Test Credentials

- **Email:** `user@vendorbridge.com`
- **Password:** `password123`

Or register a new account through the API.

## Features Implemented

### Frontend
- Landing page with hero section
- Responsive navigation
- Login page with form validation
- JavaScript integration for API calls
- CSS styling with Tailwind-inspired design

### Backend
- User authentication with JWT
- Login and registration endpoints
- Password hashing with bcrypt
- Role-based access control
- CORS support for frontend integration
- Comprehensive error handling
- API health check endpoints

## API Documentation

See [Backend/README.md](VendorBrigde/Backend/README.md) for complete API documentation.

## Development

### Add New API Endpoints

1. Create a new route file in `Backend/routes/`
2. Register it in `Backend/app.py`
3. Document the endpoint in README

### Customize Styling

Edit `Frontend/style.css` and `Frontend/css/login.css` for frontend styling.

## Production Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up a real database (PostgreSQL, MySQL)
4. Enable HTTPS
5. Configure environment variables securely
6. Implement rate limiting
7. Set up logging

## Team

Developed for the Odoo X KSV Hackathon 2026.
