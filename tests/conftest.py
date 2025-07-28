import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db, Base
from app.main import app  # ✅ Import existing app

# Create a test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Drop all tables and recreate them fresh for tests
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Override dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the default DB dependency with the test DB
app.dependency_overrides[get_db] = override_get_db

# Provide test client
@pytest.fixture
def client():
    return TestClient(app)
