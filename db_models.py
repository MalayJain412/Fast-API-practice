"""
SQLAlchemy Database Models

This file defines database table structures using SQLAlchemy ORM.
Unlike Pydantic models (which handle data validation), SQLAlchemy models:
1. Define actual database table schemas
2. Handle database operations (CRUD)
3. Manage relationships between tables
4. Provide database-specific features (indexes, constraints, etc.)
"""

# Import SQLAlchemy components for database modeling
from sqlalchemy.ext.declarative import declarative_base  # Base class for all models
from sqlalchemy import Column, Integer, String, Float    # Column types for table definition

# Create base class for all database models
# All SQLAlchemy models inherit from this Base class
# This base tracks model metadata and enables table creation
Base = declarative_base()

class Product(Base):
    """
    SQLAlchemy model representing the 'product' table in the database.
    
    This model defines:
    - Table name and structure
    - Column types and constraints
    - Primary keys and indexes
    - Database-specific configurations
    
    Key differences from Pydantic Product model:
    - This creates actual database tables and schema
    - Handles database operations and ORM queries
    - Includes database-specific features (indexes, foreign keys, constraints)
    - Used for ORM operations (create, read, update, delete)
    - Maps Python objects to database rows
    
    Inheritance from Base provides:
    - Metadata tracking for table creation
    - ORM functionality (queries, relationships)
    - Automatic table mapping
    """
    
    # Define the table name in the database
    # This will create a table called 'product' in MySQL/MariaDB
    __tablename__ = 'product'
    
    # Define table columns with their types and constraints
    # Each Column maps to a database column with specific properties
    id = Column(Integer, primary_key=True, index=True)  # Primary key with automatic indexing
    name = Column(String(255))        # Product name (max 255 characters for MySQL compatibility)
    description = Column(String(255)) # Product description (max 255 characters)
    price = Column(Float)             # Product price (floating point number)
    quantity = Column(Integer)        # Available quantity (integer)
    
    # Detailed column explanations:
    # - primary_key=True: Makes this column the unique identifier and auto-incrementing
    # - index=True: Creates database index for faster lookups and queries
    # - String(255): MySQL/MariaDB requires length specification for VARCHAR columns
    # - Float: Allows decimal numbers for pricing (supports currency values)
    # - Integer: Whole numbers for quantities and IDs (no decimal places)
    
    # Additional SQLAlchemy features that could be added:
    # - nullable=False: Make columns required
    # - unique=True: Ensure unique values
    # - default=value: Set default values
    # - ForeignKey: Create relationships between tables
    # - CheckConstraint: Add validation rules at database level
