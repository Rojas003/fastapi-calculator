# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.
Secure User Registration
Implemented a /register route using FastAPI, SQLAlchemy, and Pydantic.

User data is validated and stored in a local SQLite database (test.db).

Passwords are securely hashed using passlib[bcrypt].

Pydantic EmailStr is used to enforce proper email format.

The database schema is created automatically using SQLAlchemy models.

 Folder Structure Enhancements
Added app/models/user.py – defines the User SQLAlchemy model.

Added app/schemas/user.py – defines the Pydantic schema used for validation.

Added app/utils/security.py – handles password hashing logic.

 Test Coverage & Integration Testing
Created /tests/integration/test_main.py to verify the /register endpoint works correctly.

All tests pass successfully ( 10 passed).

Test coverage is currently 74%, and a coverage report is generated in the htmlcov/ folder.

Dependency Updates
If you're running this project locally, make sure to install the updated dependencies:
pip install -r requirements.txt

User Registration and Authentication
Implemented a /register route using FastAPI.

Added secure password hashing using Passlib (bcrypt).

Created and connected a User SQLAlchemy model.

Integrated Pydantic schemas for user input validation.

Updated user.py, schemas/user.py, and database.py accordingly.

Calculation History with Database
Created SQLAlchemy Calculation model.

Added crud/calculation.py for handling DB logic.

Set up schemas/calculation.py for input/output validation.

Implemented /calculations route to save and return operations.

Connected to PostgreSQL using SQLAlchemy and .env config.

Testing
Added integration tests to verify user and calculation routes.

Created conftest.py for test database handling.

Final test run: 11 tests passed 

 Docker and CI/CD
Created Dockerfile for containerization.

Verified image builds correctly and runs FastAPI app.

Configured GitHub Actions for:

Continuous Integration (CI) with pytest.

Docker image build and push (if configured).

Screenshot-ready for both workflow success and Docker Hub image.

### What Was Completed Today (Final Backend Stage)

- Fixed all BREAD (Browse, Read, Edit, Add, Delete) endpoints for `/calculations`
- Implemented and cleaned up `crud/calculation.py` with full logic (create, read, update, delete)
- Fixed Python import issues, including `app.models` and `app.auth`
- Created a temporary `get_current_user()` function to simulate JWT login
- Verified all FastAPI routes using `/docs`
- Wrote and successfully ran integration test for calculation creation using `pytest`
- Fixed `test_calculation.py` to include proper test structure and payload handling
- Built and tested the Docker image locally using Docker Desktop
- Pushed a fresh Docker image to Docker Hub:  
   [`rojas003/fastapi-calculator`](https://hub.docker.com/r/rojas003/fastapi-calculator)
- Confirmed the container runs properly and is exposed on port `8000`

This wraps up all the backend requirements for the assignment — the system is fully functional and Docker-deployable.
Authentication Enhancements
Implemented JWT-based authentication with /register and /login routes.

Built frontend HTML forms (register.html, login.html) using Fetch API to POST JSON payloads to the FastAPI backend.

Successfully connected frontend UI to backend routes with validation and user feedback messages ( success /  errors).

 Testing Upgrades
Added comprehensive unit, integration, and end-to-end (E2E) tests:

Unit tests for password hashing and operation logic.

Integration test for the calculation API with authenticated user.

E2E test using Playwright for browser-based registration and login simulation.

Fixed all test failures and validation errors (e.g., removed deprecated user_id field from CalculationCreate).

Verified 100% passing test suite before deployment.

 GitHub Actions CI/CD
Workflow updates:

Ensured Playwright and FastAPI server run before tests.

Fixed Docker Hub push error by correcting casing in Docker username (Rojas003 ➜ rojas003).

Updated secrets and ensured successful login for automated image push.

Final GitHub Actions workflow:

 Install dependencies

 Run tests (unit, integration, E2E)

 Build Docker image

 Push image to Docker Hub

 Documentation + Screenshots
Captured screenshots for:

 GitHub Actions successful run

 Front-end Registration/Login success via browser

 Test suite passing (terminal + coverage report)
### What Was Completed Today BREAD Functions

## Features

- **User Authentication**
  - Registration and login with JWT-based authentication.
- **Calculation Management (BREAD)**
  - **Browse**: View all calculations.
  - **Read**: Retrieve individual calculations.
  - **Edit**: Update existing calculations.
  - **Add**: Create new calculations.
  - **Delete**: Remove calculations.
- **Frontend UI**
  - HTML pages for registration, login, and calculation operations.
  - Frontend forms integrated with backend API using `fetch()` requests.
- **Database**
  - SQLite database for persisting users and calculations.
- **Automated Testing**
  - **Unit Tests**: API endpoints tested with `pytest`.
  - **Playwright E2E Tests**:
    - Positive scenarios: Registration, login, calculation creation, update, and deletion.
    - Negative scenarios: Invalid login, unauthorized access, and invalid calculation inputs.
- **CI/CD Pipeline**
  - GitHub Actions workflow to run all tests.
  - Dockerized deployment with an automated push to Docker Hub.

---

## Project Structure

fastapi-calculator/
│
├── app/
│ ├── auth/
│ │ ├── jwt_bearer.py
│ │ └── jwt_handler.py
│ ├── models/
│ ├── routes/
│ ├── templates/
│ │ ├── login.html
│ │ ├── register.html
│ │ └── calculations.html
│ ├── database.py
│ └── main.py
│
├── tests/
│ ├── e2e/
│ │ ├── test_login_ui.py
│ │ ├── test_login_failure_playwright.py
│ │ ├── test_calculation_ui_positive.py
│ │ ├── test_calculation_ui_negative.py
│ │ └── test_end_to_end_register_login_calculate.py
│ └── unit/
│ └── test_calculation_negative.py
│
├── .github/workflows/test.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
## Docker Usage
- Build the Docker Image
docker build -t fastapi-calculator .

- Tag the Image
docker tag fastapi-calculator rojas003/fastapi-calculator:latest

- Push to Docker Hub
docker push rojas003/fastapi-calculator:latest

Docker Hub Link: https://hub.docker.com/r/rojas003/fastapi-calculator