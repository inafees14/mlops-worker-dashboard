import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Local fallback (when running locally)
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./local.db"

# Heroku compatibility fix
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
