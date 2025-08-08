from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash the user's password using bcrypt."""
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user with a hashed password."""
    db_user = User(
        email=user.email,
        password=get_password_hash(user.password)  #  hash before saving
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    """Fetch a user by email."""
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Validate user credentials."""
    user = get_user_by_email(db, email)
    if user and pwd_context.verify(password, user.password):  #  verify hashed password
        return user
    return None
