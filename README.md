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

