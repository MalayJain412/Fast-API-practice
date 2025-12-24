"""
Database Configuration Module

This file sets up the database connection and session management for the FastAPI application.
It handles:
1. Loading environment variables from .env file
2. Creating database connection string
3. Setting up SQLAlchemy engine and session factory
"""

# Import required modules for database operations
from sqlalchemy import create_engine     # Creates database engine for connections
from sqlalchemy.orm import sessionmaker # Factory for creating database sessions
import os                               # For accessing environment variables
from dotenv import load_dotenv          # For loading .env file into environment

# Load environment variables from .env file
# This makes variables like DB_USER, DB_PASSWORD available via os.environ
load_dotenv()

# Construct database connection string (URL)
# Format: mysql+pymysql://username:password@host:port/database_name
# Including password from environment variables for secure database connection
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:3307/{os.environ.get('DB_NAME')}"

# Create SQLAlchemy engine
# The engine is the core interface to the database
# It manages connections, connection pooling, and executes SQL statements
# This is a singleton object that should be created once per application
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Create session factory
# sessionmaker is a factory for creating database sessions
# Sessions handle transactions and provide the interface for database operations
# This factory pattern ensures consistent session configuration across the application
# Parameters explained:
#   - autocommit=False: Transactions must be explicitly committed for data safety
#   - autoflush=False: Changes aren't automatically flushed to database (manual control)
#   - bind=engine: Binds sessions to our database engine for connection management
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Usage Notes:
# - Create sessions using: db = session()
# - Always close sessions: db.close() or use try/finally blocks
# - Use dependency injection in FastAPI for automatic session management
# - Sessions are not thread-safe, create new session per request