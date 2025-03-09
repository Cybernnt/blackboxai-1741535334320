from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./fitness_inventory.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

def init_db():
    """Initialize the database, creating all tables"""
    from src.models import company, product, category, sales
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_connection():
    """Get direct database connection"""
    return engine.connect()
