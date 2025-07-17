# init_db.py

from app.database import engine
from app.models.calculation import Calculation
from app.models.user import User
from app.database import Base

# This will create all tables based on the models
Base.metadata.create_all(bind=engine)

print("Database tables created.")
