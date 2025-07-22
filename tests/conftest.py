from app.database import Base, engine

# Drop all tables and recreate them fresh for tests
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.main import FastAPI
from app.routes import calculation_routes, user_routes

# Create a test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new app instance for testing
app = FastAPI()
app.include_router(calculation_routes.router)
app.include_router(user_routes.router)
app.dependency_overrides[get_db] = override_get_db

# Provide test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
