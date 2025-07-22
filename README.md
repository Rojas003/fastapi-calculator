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
  👉 [`rojas003/fastapi-calculator`](https://hub.docker.com/r/rojas003/fastapi-calculator)
- Confirmed the container runs properly and is exposed on port `8000`

This wraps up all the backend requirements for the assignment — the system is fully functional and Docker-deployable.
