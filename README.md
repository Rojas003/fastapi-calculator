 Features
 Advanced User Management

Secure Authentication: JWT-based login system with bcrypt password hashing
User Profiles: Complete profile management with customizable information
Password Security: Secure password change with validation
User Preferences: Personalized settings for theme, language, and notifications

 Calculator Operations (Complete BREAD Implementation)

 BROWSE: View all calculations in organized list format
 READ: Retrieve and display individual calculation details
 EDIT: Update existing calculations with full validation
 ADD: Create new calculations with all mathematical operations
 DELETE: Remove calculations with confirmation and error handling

Mathematical Operations

Addition: Precise addition calculations
Subtraction: Accurate subtraction operations
Multiplication: Reliable multiplication processing
Division: Safe division with zero-division protection
Error Handling: Comprehensive input validation and error management
Real-time Results: Instant calculation with live UI updates

 Analytics & Activity Tracking

Activity Dashboard: Real-time user activity monitoring
Usage Statistics: Comprehensive analytics and trends
Action Logging: Automatic tracking of all user actions
History Management: Filterable activity history with cleanup tools
Performance Monitoring: Request duration and success rate tracking

 Professional UI/UX

Responsive Design: Modern, mobile-friendly interface
Theme System: Light/dark mode with auto-detection
Real-time Validation: Instant form validation and feedback
Interactive Dashboard: Dynamic statistics and data visualization
Multi-language Support: Framework for internationalization

 Technical Excellence

Database Migrations: Alembic-powered schema management
Middleware Integration: Automatic activity tracking
API Documentation: Auto-generated OpenAPI/Swagger docs
Error Handling: Comprehensive exception management
Logging System: Professional-grade logging and monitoring
Technology Stack
Backend

FastAPI - Modern, fast web framework for building APIs
SQLAlchemy - Powerful ORM for database operations
Alembic - Database migration management
JWT - Secure token-based authentication
Bcrypt - Industry-standard password hashing

Frontend

HTML5/CSS3 - Modern web standards
JavaScript ES6+ - Dynamic user interactions
Fetch API - RESTful API communication
Responsive Design - Mobile-first approach

Database & Storage

SQLite - Lightweight, serverless database (easily configurable to PostgreSQL/MySQL)
SQLAlchemy Models - Robust data modeling with relationships

Testing & Quality

pytest - Comprehensive testing framework
Playwright - End-to-end browser automation
Coverage.py - Code coverage analysis
GitHub Actions - Continuous integration and deployment

DevOps & Deployment

Docker - Containerized deployment
GitHub Actions - CI/CD pipeline
Docker Hub - Container registry
Installation & Setup
Prerequisites

Python 3.13+
Git
Docker (optional)

Local Development
1. Clone the repository 
git clone https://github.com/your-username/fastapi-calculator
cd fastapi-calculator
2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install ependencies 
pip install -r requirements.txt
4. Set up environment variables 
# Create .env file
cat > .env << EOF
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=a-string-secret-at-least-256-bits-long
ALGORITHM=HS256
EOF
5. Initialize databse
# Run migrations
alembic upgrade head
6. Start the application 
uvicorn app.main:app --reload
7. Access the application 
Web Interface: http://127.0.0.1:8000
API Documentation: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
Testing 
# Complete test suite (63 tests)
pytest -v
Test Categories 
# Unit tests (business logic)
pytest tests/unit/ -v

# Integration tests (API endpoints)
pytest tests/integration/ -v

# End-to-end tests (user workflows)
pytest tests/e2e/ -v
Test Coverage
# Generate coverage report
pytest --cov=app --cov-report=html
open htmlcov/index.html
Test Results

63/63 tests passing 
Comprehensive coverage across all features
Automated UI testing with Playwright
Performance validation included

 Docker Deployment
 # Pull and run from Docker Hub
docker run -p 8000:8000 rojas003/fastapi-calculator:latest
Building locally 
# Build the image
docker build -t fastapi-calculator .

# Run the container
docker run -p 8000:8000 fastapi-calculator
Docker Hub Repository
 rojas003/fastapi-calculator
 Key Endpoints
Authentication

POST /users/register - Create new account
POST /users/login - Authenticate user

User Management

GET /users/profile - Get user profile
PUT /users/profile - Update profile information
PUT /users/change-password - Change password
GET /users/preferences - Get user preferences
PUT /users/preferences - Update preferences

Calculations

GET /calculations - List all calculations
POST /calculations - Create new calculation
GET /calculations/{id} - Get specific calculation
PUT /calculations/{id} - Update calculation
DELETE /calculations/{id} - Delete calculation

Activity & Analytics

GET /users/activity - Get activity history
GET /users/activity/stats - Get usage statistics
DELETE /users/activity - Clean up old activities

Interactive Documentation
Visit /docs when running the application for full interactive API documentation.

Project architecture 
fastapi-calculator/
├── app/
│   ├── auth/                   # Authentication & JWT handling
│   │   ├── dependencies.py     # Auth dependencies
│   │   ├── jwt_bearer.py       # JWT middleware
│   │   └── jwt_handler.py      # Token management
│   ├── core/                   # Core configuration
│   │   ├── config.py           # Application settings
│   │   └── __init__.py
│   ├── middleware/             # Custom middleware
│   │   ├── activity_middleware.py # Activity tracking
│   │   └── __init__.py
│   ├── models/                 # Database models
│   │   ├── activity_log.py     # Activity logging model
│   │   ├── calculation.py      # Calculation model
│   │   ├── user.py            # User model
│   │   └── __init__.py
│   ├── routes/                 # API routes
│   │   ├── activity_routes.py  # Activity endpoints
│   │   ├── calculation.py      # Calculation endpoints
│   │   ├── user_routes.py      # User endpoints
│   │   └── __init__.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── activity_log.py     # Activity schemas
│   │   ├── calculation.py      # Calculation schemas
│   │   ├── user.py            # User schemas
│   │   └── __init__.py
│   ├── services/               # Business logic
│   │   ├── activity_service.py # Activity management
│   │   └── __init__.py
│   ├── utils/                  # Utilities
│   │   ├── operations.py       # Mathematical operations
│   │   ├── security.py         # Security utilities
│   │   └── __init__.py
│   ├── database.py             # Database configuration
│   └── main.py                 # Application entry point
├── alembic/                    # Database migrations
│   ├── versions/               # Migration files
│   ├── env.py                  # Alembic configuration
│   └── script.py.mako
├── templates/                  # HTML templates
│   ├── activity.html           # Activity dashboard
│   ├── calculation.html        # Calculator interface
│   ├── login.html             # Login page
│   ├── preferences.html        # User preferences
│   ├── profile.html           # User profile
│   └── register.html          # Registration page
├── tests/                      # Test suite
│   ├── e2e/                   # End-to-end tests
│   ├── integration/           # Integration tests
│   ├── unit/                  # Unit tests
│   └── conftest.py            # Test configuration
├── .github/workflows/          # CI/CD pipeline
│   └── test.yml               # GitHub Actions workflow
├── .env                       # Environment variables
├── alembic.ini               # Alembic configuration
├── Dockerfile                # Docker configuration
├── pytest.ini               # Pytest configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
CI/CD Pipeline
GitHub Actions Workflow

✅ Automated Testing - Full test suite on every push
✅ Code Quality - Linting and formatting checks
✅ Docker Build - Automatic container building
✅ Deployment - Push to Docker Hub on success
✅ Playwright Tests - Browser automation testing

Pipeline Features

Multi-environment testing (Python 3.13)
Dependency caching for faster builds
Parallel test execution
Automatic browser installation for UI tests
Secure credential management

 Key Features & Innovations
 User Experience

Real-time Theme Switching - Instant dark/light mode toggle
Activity Monitoring - Track every user action automatically
Usage Analytics - Personal dashboard with statistics
Preference Management - Customizable user settings
Professional UI - Modern, responsive design

 Technical Innovation

Automatic Activity Tracking - Middleware-based action logging
Advanced Database Design - Complex relationships and migrations
Comprehensive Testing - 63 tests covering all scenarios
Security Best Practices - JWT, bcrypt, input validation
Production Architecture - Professional-grade code organization

 Analytics & Monitoring

User Activity Dashboard - Real-time statistics and trends
Performance Tracking - Request duration and success rates
Usage Patterns - Login frequency and action analytics
Data Management - Automatic cleanup and archival

 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request
 License
This project is licensed under the MIT License - see the LICENSE file for details.
 Author
Sherry Rojas

GitHub: @Rojas003
Docker Hub: rojas003

Academic Achievement
This project was developed as a final assignment demonstrating mastery of:

 Full-stack web development with modern frameworks
 Database design and ORM usage
 Authentication and security implementation
 Comprehensive testing strategies
 DevOps practices and containerization
 Software engineering best practices

Final Test Score: 63/63 Passing Tests 

Quick start commands
# Clone and setup
git clone https://github.com/your-username/fastapi-calculator
cd fastapi-calculator
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run migrations and start
alembic upgrade head
uvicorn app.main:app --reload

# Test everything
pytest -v

# Docker deployment
docker run -p 8000:8000 rojas003/fastapi-calculator:latest

 Ready to explore? Visit http://localhost:8000 and start calculating!