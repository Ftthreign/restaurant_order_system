from sqlalchemy import create_engine, text
from app.config import settings

print("Testing database connection...")
print(f"Database URL: {settings.DATABASE_URL}")

try:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful:", result.fetchone())
except Exception as e:
    print("Database connection failed:", e)
