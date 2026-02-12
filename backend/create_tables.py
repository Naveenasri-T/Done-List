"""
Create all database tables
Run this script once to initialize the database
"""
from app.database import engine, Base
from app.models import *  # Import all models

def create_tables():
    """Create all tables defined in models"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

if __name__ == "__main__":
    create_tables()
