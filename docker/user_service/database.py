# database.py
"""
This module contains the database configuration and session management for the application.
It defines the connection to the PostgreSQL database -
and provides a sessionmaker for interacting with the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import base64

# SQLALCHEMY_DATABASE_URL is the connection string for the PostgreSQL database.
# For local testing:
# SQLALCHEMY_DATABASE_URL = "postgresql://andyg:@localhost:5432/postgres"
# For the Docker Compose setup:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/app_db"
# For the k8s:
# SQLALCHEMY_DATABASE_URL ="postgresql://user:password@postgres-service:5432/app_db"
# For EKS:
DB_USERNAME = os.getenv("DB_USERNAME")
DB_ENDPOINT = os.getenv("DB_ENDPOINT")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME     = os.getenv("DB_NAME")

DB_USERNAME = base64.b64decode(DB_USERNAME).decode('utf-8')
DB_ENDPOINT = base64.b64decode(DB_ENDPOINT).decode('utf-8')
DB_PASSWORD = base64.b64decode(DB_PASSWORD).decode('utf-8')
DB_NAME     = base64.b64decode(DB_NAME).decode('utf-8')

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}"


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

User_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency function to get a database session.

    This function can be used as a dependency in FastAPI routes to provide a
    database session for each request. It ensures that the session is closed
    after the request is processed.

    Returns:
        Session: A SQLAlchemy session object.
    """
    db = User_Session()
    try:
        yield db
    finally:
        db.close()
