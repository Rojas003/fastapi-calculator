import pytest
import multiprocessing
import time
import uvicorn
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.main import app

# Use a different database for tests to avoid conflicts
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_pytest.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Setup test database for the entire test session"""
    # Remove existing test db
    if os.path.exists("./test_pytest.db"):
        os.remove("./test_pytest.db")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    
    # Cleanup after tests
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_pytest.db"):
        os.remove("./test_pytest.db")

def override_get_db():
    """Override database dependency for tests"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

def run_uvicorn():
    """Run uvicorn server for Playwright tests"""
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error", reload=False)
    except Exception as e:
        print(f"Server failed to start: {e}")

def needs_server():
    """Check if we need to start a server for these tests"""
    import sys
    # Check command line args and environment
    playwright_indicators = [
        "playwright", "ui", "chromium", "test_calculation_ui", 
        "test_login", "test_register", "test_login_failure"
    ]
    
    # Check sys.argv
    for arg in sys.argv:
        if any(indicator in arg.lower() for indicator in playwright_indicators):
            return True
    
    # Check pytest markers
    try:
        # If we have access to pytest config, check for markers
        import _pytest
        return True  # Default to starting server if unsure
    except:
        return True

@pytest.fixture(scope="session", autouse=True)
def start_test_server():
    """Start test server for Playwright tests"""
    # Always start server - it's better to be safe
    server_process = None
    
    try:
        # Check if server is already running
        import requests
        response = requests.get("http://127.0.0.1:8000", timeout=1)
        print("Server already running")
        yield
        return
    except:
        pass  # Server not running, we'll start it
    
    try:
        print("Starting test server...")
        server_process = multiprocessing.Process(target=run_uvicorn)
        server_process.start()
        
        # Wait for server to start with retries
        import requests
        for i in range(10):  # Try for 10 seconds
            try:
                response = requests.get("http://127.0.0.1:8000", timeout=1)
                print(f"Test server ready on attempt {i+1}")
                break
            except:
                time.sleep(1)
        else:
            print("Warning: Test server may not have started properly")
        
        yield
        
    finally:
        if server_process:
            print("Stopping test server...")
            server_process.terminate()
            server_process.join(timeout=5)
            if server_process.is_alive():
                server_process.kill()
                server_process.join()

# Alternative: Simpler fixture that always starts server
@pytest.fixture(scope="session")
def live_server():
    """Alternative fixture to explicitly start server"""
    server_process = multiprocessing.Process(target=run_uvicorn)
    server_process.start()
    time.sleep(3)  # Give server time to start
    yield "http://127.0.0.1:8000"
    server_process.terminate()
    server_process.join()