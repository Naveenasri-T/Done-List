"""Test database connection"""
from app.database import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✓ Database connection successful!")
        print(f"Result: {result.fetchone()}")
        
        # Try to query users table
        result = connection.execute(text("SELECT COUNT(*) FROM users"))
        count = result.fetchone()[0]
        print(f"✓ Users table exists with {count} users")
        
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    import traceback
    traceback.print_exc()
